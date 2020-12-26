# Website Advanced Search engine

This project represents the idea of typical QA system nowadays. It combines the idea of retrieval models and latest QA solutions.  
It builds website-specific index to search on top of and provides precise answers for the end-user.  

## Use case

1. Allow user to search for information on a website via native language.  
2. The user expects precise answer on his question.  
3. The system must suggest a link to the page the information was found on.  

## Future work

1. Add Question-Answering model for Russian language (DeepPavlov does not have one).  
2. Fine-tune model for specific area of interest (e-commerce, company-products, etc.)  
3. Create website-plugin instead of chrome extension to be natively loaded with the website.  
4. Replace tf-idf with other, more production-ready tools.  

## References

1. [https://blog.griddynamics.com/question-answering-system-using-bert/](https://blog.griddynamics.com/question-answering-system-using-bert/)  
2. [https://blog.griddynamics.com/vs-model-for-ecommerce/](https://blog.griddynamics.com/vs-model-for-ecommerce/)  
3. [Similar product](https://blog.tensorflow.org/2020/03/exploring-helpful-uses-for-bert-in-your-browser-tensorflow-js.html)
