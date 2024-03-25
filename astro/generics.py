# coding=utf-8
"""
Created on 2020, May 1th
@author: orion
"""
import django.db as db
import django.core.exceptions as exception
from django.db import models


class Debugger(object):
    
    def __init__(self, **kwargs):
        
        if kwargs:
            if 'is_test' in kwargs:
                self.is_test = True
            else:
                self.is_test = False
        else:
            self.is_test = False
            
    def is_debugger_active_for_test(self):
        return self.is_test
    
    def set_debugger_active_for_test(self):
        self.is_test =True

###############################################################################
def returned_var_as_list(var):

    if isinstance(var, list):
        varlist = var
    else:
        varlist = [var]
        
    return varlist
             
###############################################################################
def tagscorrection(tags):

    wtags = []
    if len(tags.split(',')) == 1:
        wtags.append(tags.encode('utf8'))
    else:
        for tag in tags:
            wtags.append(tag.encode('utf8'))
        
    return wtags

###############################################################################
def returned_code_ko_task_aborted():
    
    success = False
    message = "La publication source n'a pas été identifiée => la réflexion réponse ne pouvant pas être publiée. La tâche demandée ne peut pas être prise en compte dans la BD"
    code = u""
    
    return success, code, message
  
###############################################################################  
def returned_code_ok_already_in_db():
    
    success = True
    message = "L'enregistrement existe déjà dans la Base de Données => il n'a donc pas été nécessaire de l'ajouter"
    code = u""
    
    return success, code, message
   
###############################################################################
def returned_code_ko_not_in_db():
    
    success = False
    message = "L'enregistrement demandé n'existe pas dans la Base de Données"
    code = u""
    
    return success, code, message
  
###############################################################################  
def returned_code_ok():
    
    success = True
    message = u"L'action demandée a été exécutée avec succès"
    code = u""
    
    return success, code, message
###############################################################################
class ReturnedCode(object):
    
    """
       Classe générique qui permet de gérer les informations retour, de façon 
       cohérente lors des appels de fonctions
       
    """
    def __init__(self, calling_function_name, success, code, message):
        self.calling_function_name = calling_function_name
        self.success = success
        self.message = message  
        self.code = code

###############################################################################
def get_returned_code_ok_object():
    name = u"get_returned_code_ok_object"
    success, code, message = returned_code_ok()
    return ReturnedCode(name, success, code, message)
###############################################################################

def manage_save_exception(calling_function_name, mymodel):
    """
    Fournit un code de gestion du traitement des exceptions après un save
    sur un Modèle
    """
    name = calling_function_name + u" / manage_save_exception"
    
    try:
        mymodel.save()
        
    except db.IntegrityError as e:
        success = False
        code = e.__class__.__name__
        message = e.message
    except db.Error as e:
        success = False
        code = e.__class__.__name__
        message = e.message
    except db.DataError as e:
        success = False
        code = e.__class__.__name__
        message = e.message
    except TypeError as e:
        success = False
        code = e.__class__.__name__
        message = e.message
    except exception.FieldError as e:
        success = False
        code = e.__class__.__name__
        message = e.message
    except models.ProtectedError as e:
        success = False
        code = e.__class__.__name__
        message = e.message
    except db.Error as e:
        success = False
        code = e.__class__.__name__
        message = e.message         
    except db.DatabaseError as e:
        success = False
        code = e.__class__.__name__
        message = e.message   
    except db.OperationalError as e:
        success = False
        code = e.__class__.__name__
        message = e.message   
    except db.InterfaceError as e:
        success = False
        code = e.__class__.__name__
        message = e.message   
    except db.InternalError as e:
        success = False
        code = e.__class__.__name__
        message = e.message           
    except db.ProgrammingError as e:
        success = False
        code = e.__class__.__name__
        message = e.message   
    except db.NotSupportedError as e:
        success = False
        code = e.__class__.__name__
        message = e.message       

    else:
        success, code, message = returned_code_ok()
    
    return ReturnedCode(name, success, code, message)
    
###############################################################################
def manage_existence_exception(calling_function_name, var):
    """
    Fournit un code de gestion du traitement des exceptions après un save
    sur un Modèle
    """
    name = calling_function_name + u" / manage_existence_exception"

    try:
        var
        
    except NameError as e:
        success = False
        code = e.__class__.__name__
        message = e.message     

    else:
        success, code, message = returned_code_ok()
    
    return ReturnedCode(name, success, code, message)
