import re
class TextPipe(object):
    """
    Make a pipeline for text normalization. Apply a function to
    a set of documents, return the result or just update the documents attribute
    inside the object. Helps preprocessing text data and simplifies code.
    
    Parameters
    ----------
    documents : array, list
        Array of strings.
    keys : array, list, pandas.Series
        Numeric or string value to label each document.
    store_raw : bool, optional (default=False)
        Store initially supplied data to reset.
    
    Attributes
    ----------
    self.documents : dict
        List of processed documents. Each Item is a list of strings.
    self.ops : dict
        Instructions performed on data with order.
    self.ops_target : dict
        The target of the instructions, whether applied to documents or words.
    """
    def __init__(self,documents,keys):
        self.documents = dict(zip(keys,documents))
        self.ops = {}
        self.ops_target = {}
        self.__ops_counter__ = 1
    
    def apply(self,documents,fun,*args):
        """
        Main function for apply family.
        """
        for key in documents.keys():
            documents[key] = fun(documents[key],*args)
        return documents
    
    def apply_docs(self,fun,*args,output=False,data=None,applier="doc"):
        """
        Apply a specified function to documents.
        
        Parameters
        ----------
        fun : callable
            Any callable to invoke. Whatever specified here will be fed with
            documents as first argument.
        *args : positional arguments
            Arguments of 'fun'.
        output : bool, optional (default=False)
            True if return result after the operation, False if update the 
            attribute 'documents' with this result.
        data : array, list, ignores 'output'
            Use an external data and return the result.
        """
        if output or data is not None:
            return self.apply(self.documents.copy() if data is None else data.copy(),fun,*args)
        else:
            self.documents = self.apply(self.documents,fun,*args)
            self.ops[self.__ops_counter__] = fun
            self.ops_target[self.__ops_counter__] = applier
            self.__ops_counter__ += 1
        
    def apply_words(self,fun,*args,output=False,data=None):
        """
        Apply a specified function to words of documents.
        
        Parameters
        ----------
        fun : callable
            Any function to invoke. Whatever specified here will be fed with
            documents as first argument.
        *args : positional arguments
            Arguments of 'fun'.
        output : bool, optional (default=False)
            True if return result after the operation, False if update the 
            attribute 'documents' with this result.
        data : array, list, ignores 'output'
            Use an external data and return the result.
        """
        return self.apply_docs(fun=lambda doc:[fun(word,*args) for word in doc],output=output,data=data,applier="word")
        
    def filter_none(self):
        """
        Filter None documents and words.
        """
        self.filter_none_stats = {"documents":[],"words":0}
        for key in list(self.documents):
            if self.documents[key] == None:
                del self.documents[key]
                self.filter_none_stats["documents"].append(key)
            else:
                init_len = len(self.documents[key])
                self.documents[key] = [word for word in self.documents[key] if not word == None]
                self.filter_none_stats["words"] += init_len - len(self.documents[key])
            
        self.ops[self.__ops_counter__] = "Filter None >> Documents:" + str(len(self.filter_none_stats["documents"])) + " Words:" + str(self.filter_none_stats["words"])
        self.ops_target[self.__ops_counter__] = "filter_none"
        self.__ops_counter__ += 1
        
    def pipeline(self,*args):
        """
        Execute whole pipeline to specified data.
        """
        docs = TextPipe(*args)
        for target,fun in zip(self.ops_target.values(),self.ops.values()):
            if target == "filter_none":
                docs.filter_none()
            else:
                docs.apply_docs(fun)
        return docs.documents
    
    def save(self,filename,external_vars=None):
        try:
            import dill
            if len(self.ops) == 0 or len(self.ops_target) == 0:
                raise AttributeError('Build a pipeline first.')
                
            tmp = {'inst':{'ops':self.ops,'ops_target':self.ops_target},
                   'vars':external_vars}
            with open(filename, 'wb') as f:
                dill.dump(tmp, f)
                
        except ModuleNotFoundError:
            print('Module `dill` is required to save pipelines.')
        
    def load(self,filename):
        try:
            import dill
            with open(filename,'rb') as f:
                tmp = dill.load(f)
            
            self.ops = tmp['inst']['ops']
            self.ops_target = tmp['inst']['ops_target']
            
            if tmp['vars'] is not None:
                for key,item in tmp['vars'].items():
                    globals()[key] = item
            
        except ModuleNotFoundError:
            print('Module `dill` is required to load pipelines.')
            
