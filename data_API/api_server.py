import tornado.ioloop
import tornado.web
import http
http.socket_timeout = 9999
import time
import pickle
import time
import json
from  tornado.escape import json_decode
from  tornado.escape import json_encode
from tornado.concurrent import Future
from tornado import gen
from tornado.options import define, options, parse_command_line
import requests
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd
from pathlib import Path  
import glob
from sklearn.metrics.pairwise import cosine_similarity
import numpy
from rdflib import Graph
from flashtext import KeywordProcessor
import re
import numpy as np

# Loadinb Brick Schema
g = Graph()
g.parse("data/Brick.ttl", format="turtle")

def vectorize(list_of_docs):
    vectorizer = TfidfVectorizer()
    vectors = vectorizer.fit_transform(list_of_docs)
    feature_names = vectorizer.get_feature_names_out()
    dense = vectors.todense()
    denselist = dense.tolist()
    df = pd.DataFrame(denselist, columns=feature_names)
    return df, vectorizer

def indexing_brick():
    definitions = {}
      
    try:
        df = pd.read_csv('model.csv', header=None)
        #df = df.drop_duplicates()

        model = {}
        for index, row in df.iterrows():
            model[row[2]]=str(row[0])+" "+str(row[1])    
    except:
        model = {}

    for triple in g:
        if "definition" in triple[1]:
            class_name = triple[0].replace("https://brickschema.org/schema/Brick#","")
            definition = triple[2]
            class_name = class_name.replace("_"," ")
            try:
                definitions[class_name] = definition+" "+ class_name+ " " + model[class_name]
            except:
                definitions[class_name] = definition+" "+ class_name

        elif "#Location" in triple[2]:
            class_name = triple[0].replace("https://brickschema.org/schema/Brick#","")
            definition = class_name
            class_name = class_name.replace("_"," ")
            try:
                definitions[class_name] = definition +" " + class_name + " " + model[class_name]
            except:
                definitions[class_name] = definition +" " + class_name + " "

    for key in definitions.keys():
        if str(definitions[key]).startswith("See"):
            definitions[key] = definitions[definitions[key].split(" ")[1].replace("_"," ")]
            #print("->",definitions[key])
    
    #print(definitions)
    list_of_classname = []
    list_of_definitions = []
    
    for key in definitions.keys():
        list_of_classname.append(key)
        list_of_definitions.append(definitions[key])
  
    df_class, vectorizer_class = vectorize(list_of_classname)
    df_def, vectorizer_def = vectorize(list_of_definitions)

    return df_class, df_def, vectorizer_class, vectorizer_def, list_of_classname, list_of_definitions
        
df_class, df_def, vectorizer_class, vectorizer_def, list_of_classname, list_of_definitions = indexing_brick()
print("* Loading Done")

list_of_valid_locations = []
for triple in g:
    if "#Location" in triple[2] and "https://brickschema.org/schema/Brick#hasAssociatedTag" in triple[1]:
        list_of_valid_locations.append(triple[0].replace("https://brickschema.org/schema/Brick#",""))
print(list_of_valid_locations)

def search_locations(query, topk=1):
    if "room" in query.lower():
        query+=" room"
    query_vec = vectorizer_class.transform([query])
    search_result = {}
    idx = 0
    for index, row in df_class.iterrows():
        class_name = list_of_classname[idx]
        similarity = cosine_similarity(row.values.reshape(1,len(row.values)), query_vec.toarray())[0][0]
        search_result[class_name]=similarity
        idx+=1

    search_result = dict(sorted(search_result.items(), key=lambda item: item[1], reverse=True))
    return_list = []
    rank=1
    for key in search_result.keys():
        if key in list_of_valid_locations:
            return_list.append((key,search_result[key]))
            if rank==topk: break
            rank+=1
    if return_list[0][1]==0.0:
        return_list= [('Location', 1,0)]
    return return_list

def search(query, hint="", topk=20):
    query = parse_label(query)

    return_list = []
    '''
    parsed_query = query.split(" ")
    for classname in list_of_classname:
        cnt = 0
        for term in parsed_query:
            if term in classname:
                cnt+=1
        if cnt==len(parsed_query):
            return_list.append((classname,cnt))
    '''
    
    
    search_result = {}
    idx = 0
    
    query_vec = vectorizer_def.transform([query])
    
    for index, row in df_def.iterrows():
        class_name = list_of_classname[idx]
        similarity = cosine_similarity(row.values.reshape(1,len(row.values)), query_vec.toarray())[0][0]
        search_result[class_name]=similarity
        idx+=1

    idx = 0
    query_vec = vectorizer_class.transform([query])
    
    for index, row in df_class.iterrows():
        class_name = list_of_classname[idx]
        similarity = cosine_similarity(row.values.reshape(1,len(row.values)), query_vec.toarray())[0][0]
        search_result[class_name]+=similarity
        idx+=1

    search_result = dict(sorted(search_result.items(), key=lambda item: item[1], reverse=True))
    
    rank=1
    for key in search_result.keys():
        return_list.append((key,format(search_result[key], '.2f')))
        if rank==topk: break
        rank+=1
    return return_list

def get_metadata_csv(filename='NIST_metadata_cleaned.csv'):
    
    list_of_rows = []
    
    data = pd.read_csv(filename)
    data = data.fillna('NONE')
    for index, row in data.iterrows():
        list_of_rows.append([row[1],row[2]])
        
    return list_of_rows

def get_rel_list():
    rel_list = []
    for triple in g:
        if "brick" in triple[0] and "22-rdf-syntax-ns#type" in triple[1] and ("AsymmetricProperty" in triple[2] or "ObjectProperty" in triple[2]):
            rel_list.append(triple[0].replace("https://brickschema.org/schema/Brick#",""))
    rel_list = list(set(rel_list))
    rel_list.sort()
    
    return rel_list

class GetRelListHandler(tornado.web.RequestHandler):
    
     def post(self):
        json_obj = json_decode(self.request.body)
        rel_list = get_rel_list()        
        response_to_send = {"rel_list":rel_list}        
        self.write(json.dumps(response_to_send))

class GetMetadataCSVHandler(tornado.web.RequestHandler):
    
     def post(self):
        json_obj = json_decode(self.request.body)
        input_file = json_obj['input_file']
        list_of_rows = get_metadata_csv(input_file)           
        response_to_send = {"list_of_rows":list_of_rows}
        
        self.write(json.dumps(response_to_send))

class SearchHandler(tornado.web.RequestHandler):
    
     def post(self):
        json_obj = json_decode(self.request.body)
        search_kwd = json_obj['search_kwd']
        print(search_kwd)
        response_to_send = {}
        response_to_send['result'] = search(search_kwd)
        self.write(json.dumps(response_to_send))

class CreateCheckpointHandler(tornado.web.RequestHandler):
    
     def post(self):
        json_obj = json_decode(self.request.body)
        print(json_obj)

        response_to_send = {}
        response_to_send['endcode'] = 0

        try:
            json_string = json.dumps(json_obj)
                # Using a JSON string
            with open(json_obj['filename'], 'w') as outfile:
                outfile.write(json_string)
        except:
            response_to_send['endcode'] = 1
            
        self.write(json.dumps(response_to_send))

class SaveBrickHandler(tornado.web.RequestHandler):
    
     def post(self):
        json_obj = json_decode(self.request.body)
        print("----")
        print(json_obj)
        print("----")
        ttl=""
        header = """@prefix bldg: <https://url_of_this_data#> .
@prefix brick: <https://brickschema.org/schema/1.1/Brick#> . 
@prefix btag: <https://brickschema.org/schema/1.0.2/BrickTag#> .
@prefix gtc: <https://brickschema.org/schema/1.0.2/building_example#> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix tag: <https://brickschema.org/schema/1.1/BrickTag#> .
@prefix xml: <http://www.w3.org/XML/1998/namespace> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
        """
        ttl+=header+"\n"
        
        classes = json_obj['list_of_nodes']
        relationships = json_obj['list_of_rels']
        for item in classes:
            obj_name = item.split("(")[0].strip()
            brick_name = item.split("(")[1][:-1].strip()
            class_line = "bldg:"+str(obj_name).replace(" ","_")+" a brick:"+str(brick_name).replace(" ","_")+" ."
            ttl+=class_line+"\n"

        for item in relationships:
            from_node = item[1]
            to_node = item[2]
            from_node_type = from_node.split("(")[1][:-1]
            to_node_type = to_node.split("(")[1][:-1]
            from_node = from_node.split("(")[0].strip()
            to_node = to_node.split("(")[0].strip()
            rel_line = "bldg:"+from_node.replace(" ","_")+" brick:"+item[3].replace(" ","_")+" bldg:"+to_node.replace(" ","_")+" ."
            ttl+=rel_line+"\n"

        filename = json_obj['filename']
        f = open(filename,'w')
        f.write(ttl+"\n")
        f.close()

        response_to_send = {}
        response_to_send['endcode'] = 0

        self.write(json.dumps(response_to_send))


class UpdateModelHandler(tornado.web.RequestHandler):
    
     def post(self):
        json_obj = json_decode(self.request.body)
        data_label = json_obj['data_label']
        description = json_obj['description']
        brick_class = json_obj['brick_class']
        f = open('model.csv','a')
        f.write(data_label+","+description+","+brick_class+"\n")
        f.close()

        response_to_send = {}

        self.write(json.dumps(response_to_send))


class GetCheckpointHandler(tornado.web.RequestHandler):
    
     def post(self):
        json_obj = json_decode(self.request.body)
        filename = json_obj['filename']
        response_to_send = {}
        
        response_to_send['endcode'] = 0
        try:
            with open(filename) as json_file:
                data = json.load(json_file)
                response_to_send['data'] = data
                
        except:
            response_to_send['data'] = {}
            response_to_send['endcode'] = 1
            
        self.write(json.dumps(response_to_send))
'''
class SuggestAllLocationHandler(tornado.web.RequestHandler):
    
     def post(self):
        json_obj = json_decode(self.request.body)
        locations = json_obj['list_of_locations']
        ## Suggesting Brick Location Classes based on Location Names
        matched_classes = []
        idx = 0
        for location in locations:
            search_perform = search_locations(location)[0][0]
            matched_classes.append([idx, search_perform])
            idx+=1

        response_to_send = {'matched_classes': matched_classes}
        print(response_to_send)
        self.write(json.dumps(response_to_send))
'''
import re
def parse_colname(term):
    parsed = re.sub('[^a-zA-Z0-9\n\.]', ' ', term)
    return parsed

def parse_label(label):
    terms = []
    parsed = parse_colname(label.replace("_",""))
    parsed =re.sub(r"(?<=\w)([A-Z])", r" \1", parsed)
    tmp=""
    for item in parsed.split(" "):
        if len(item)>1:
            terms.append(item)
            if tmp!="":
                terms.append(tmp)
                tmp=""
        else:
            tmp +=item
    if tmp!="":
        terms.append(tmp)
        tmp=""
    return ' '.join(terms)

class SuggestSelectedHandler(tornado.web.RequestHandler):
    
     def post(self):
        json_obj = json_decode(self.request.body)
        rows = json_obj['list_of_rows']

        matched_classes = []
        idx = 0
        for row in rows:
            print(idx,"/",len(rows)," processed")
            query = str(row[1])+" "+str(row[3])
            print(query)
            search_perform = search(query,topk=1)
            matched_classes.append([row[0], search_perform])
            idx+=1
            #if idx==5: break
        response_to_send = {'matched_classes': matched_classes}
        print(response_to_send)
        self.write(json.dumps(response_to_send))

class ReIndexHandler(tornado.web.RequestHandler):
    
     def post(self):
        global df_class, df_def, vectorizer_class, vectorizer_def, list_of_classname, list_of_definitions
        df_class, df_def, vectorizer_class, vectorizer_def, list_of_classname, list_of_definitions = indexing_brick()

        response_to_send = {}
        print(response_to_send)
        self.write(json.dumps(response_to_send))

def data_api_app():
    return tornado.web.Application([
        (r"/get_metadata_csv", GetMetadataCSVHandler),
        (r"/get_rel_list", GetRelListHandler),
        (r"/search", SearchHandler),
        #(r"/suggest_all_location", SuggestAllLocationHandler),
        (r"/suggest_selected", SuggestSelectedHandler),
        (r"/create_checkpoint", CreateCheckpointHandler),
        (r"/get_checkpoint", GetCheckpointHandler),
        (r"/save_brick", SaveBrickHandler),
        (r"/update_model", UpdateModelHandler),
        (r"/reindex", ReIndexHandler),
        
    ])

if __name__ == "__main__":
    
    app = data_api_app()
    app.listen(8889)
    tornado.ioloop.IOLoop.current().start()
