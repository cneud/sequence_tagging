#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 14:40:34 2017

@author: riedlmn
"""

import configparser
import sys,os



test = {}

train = {}
train["germeval"]="/projekte/ocex/martin/NER/corpora/GermaNER-train.conll"
train["conll2003"] = "/projekte/ocex/martin/NER/corpora/new/utf8.deu.mr.train"
train["lft"]= "/projekte/ocex/martin/NER/corpora/tokenized/enp_DE.lft.mr.tok.train.bio"
train["onb"]= "/projekte/ocex/martin/NER/corpora/tokenized/enp_DE.onb.mr.tok.train.bio"
train["sbb"]= "/projekte/ocex/martin/NER/corpora/tokenized/enp_DE.sbbmr.mr.tok.train.bio"



test = {}
test["germeval.test"]="/projekte/ocex/martin/NER/corpora/GermaNER-test.conll"
test["conll.test"] = "/projekte/ocex/martin/NER/corpora/new/utf8.deu.mr.testb"
test["lft.test"]= "/projekte/ocex/martin/NER/corpora/tokenized/enp_DE.lft.mr.tok.test.bio"
test["onb.test"]= "/projekte/ocex/martin/NER/corpora/tokenized/enp_DE.onb.mr.tok.test.bio"
test["sbb.test"]= "/projekte/ocex/martin/NER/corpora/tokenized/enp_DE.sbbmr.mr.tok.test.bio"
test["germeval.dev"]="/projekte/ocex/martin/NER/corpora/GermaNER-test.conll"
test["conll.dev"] = "/projekte/ocex/martin/NER/corpora/new/utf8.deu.mr.testa"
test["lft.dev"]= "/projekte/ocex/martin/NER/corpora/tokenized/enp_DE.lft.mr.tok.dev.bio"
test["onb.dev"]= "/projekte/ocex/martin/NER/corpora/tokenized/enp_DE.onb.mr.tok.dev.bio"
test["sbb.dev"]= "/projekte/ocex/martin/NER/corpora/tokenized/enp_DE.sbbmr.mr.tok.dev.bio"


embeddings = {}
#embeddings["german_de_100"]= (100,"/projekte/ocex/martin/fastText/German_de_docs_skip_100.vec")
#embeddings["german_de_500"]= (500,"/projekte/ocex/martin/fastText/German_de_docs_skip_500.vec")
#embeddings["de_100"]= (500,"/projekte/ocex/martin/w2v/de_txt.s500.n15.skip")

#embeddings["wiki_500"] = (500,"/projekte/ocex/martin/NER/sequence_tagging3/de_tokenized_clean_w2v_skip_w5_n5_s500d.txt")


embeddings["mr_wiki_de_300"]="/projekte/ocex/martin/fastText/de_wiki.txt.seg.10.lower.txt.300.bin"
embeddings["mr_wiki_de_upper_300"]="/projekte/ocex/martin/fastText/de_wiki.txt.seg.10.txt.300.bin"
#embeddings["facebook_de"]="/projekte/ocex/martin/embeddings/fasttext/wiki.de.bin"
#embeddings["German_de_300"]="/projekte/ocex/martin/fastText/German_de_docs_skip_300.bin"

configfile = sys.argv[1]

param = configparser.SafeConfigParser()
param.read(configfile)

for train_key,train_val in train.items():
    for emb_key,emb_val in embeddings.items():
        emb_dim = 300
        out_dir = "train3_"+train_key+"_"+emb_key
        #out_dir = "train_"+train_key+"_"+emb_key
        
        if not os.path.exists(out_dir):
            os.makedirs(out_dir)
        param.set("PARAM","use_chars","True")
        param.set("PATH","dir_model_output",out_dir)
        param.set("PATH","dir_vocab_output",out_dir)
        param.set("PATH","path_log",out_dir+ "/test.log")
        param.set("PATH","filename_train",train_val)
        param.set("PATH","filename_dev","all_conll_germeval_europeana")
        param.set("EMBEDDINGS","dim_word",str(emb_dim))
        param.set("EMBEDDINGS","filename_glove",emb_val)
        param.set("EMBEDDINGS","filename_trimmed",emb_val+".trimmed.npz")
        new_config_file = out_dir+"/config_"+train_key+"_"+emb_key
        param.write(open(new_config_file,"w"))
        print("python build_data.py "+ new_config_file)
        print("python train.py "+ new_config_file)
        for (t,tf) in test.items():
            print("python test.py "+new_config_file+ " "+tf + " > "+out_dir+ "/"+t+".res")
        for (t,tf) in test.items():
            print("python test.py "+new_config_file+ " "+tf.replace("test","dev") + " > "+out_dir+ "/"+t.replace("test","dev")+".res")
        #for (t,tf) in train.items():
        #    print("python test.py "+new_config_file+ " "+tf + " > "+out_dir+ "/"+t+".train"+".res")
        
        