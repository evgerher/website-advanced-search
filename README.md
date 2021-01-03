# Website Advanced Search engine

This project represents the idea of typical QA system nowadays. It combines the idea of retrieval models and latest QA solutions.  
It builds website-specific index to search on top of and provides precise answers for the end-user.  


## Demo

![Application demonstration](.github/demo.gif)

---

## Use case

1. Allow user to search for information on a website via native language.  
2. The user expects precise answer on his question.  
3. The system must suggest a link to the page the information was found on.  

## Instructions to run example

1. Install `requirements.txt` 
2. Download `en-core-web-md` SpaCy dataset via `python -m spacy download en_core_web_md`  
3. Install package locally `pip install -e .`  
4. Start server `FLASK_APP=server flask run`  
5. Install google chrome extension from local files  
    1. Open google chrome.
    2. Go to `Settings -> Extensions`
    3. Enable `Developer mode`  
    4. Click `Load unpacked` and select folder `client`  
6. Open new tab and click on the extension, write queries about cooking.  
    1. Queries w/o `?` mark in the end will be treated as a search for matching recipe (Ctrl-click one of them).  
    2. Query with `?` mark in the end are Question-Answer request and the answer will appear in the same block.  

## Instructions to build

1. Apply steps 1-3 from previous instructions
2. ... 

---

## Future work

1. Add Question-Answering model for Russian language (DeepPavlov does not have one).  
2. Fine-tune model for specific area of interest (e-commerce, company-products, etc.)  
3. Create website-plugin instead of chrome extension to be natively loaded with the website.  
4. Replace tf-idf with other, more production-ready tools.  

## References

1. [https://blog.griddynamics.com/question-answering-system-using-bert/](https://blog.griddynamics.com/question-answering-system-using-bert/)  
2. [https://blog.griddynamics.com/vs-model-for-ecommerce/](https://blog.griddynamics.com/vs-model-for-ecommerce/)  
3. [Similar product](https://blog.tensorflow.org/2020/03/exploring-helpful-uses-for-bert-in-your-browser-tensorflow-js.html)
