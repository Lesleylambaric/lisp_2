"""
LISP Interpreter 
"""
#!/usr/bin/env python3
import sys
sys.setrecursionlimit(20_000)



import sys
import doctest
from typing import Any

sys.setrecursionlimit(20_000)

# NO ADDITIONAL IMPORTS!

#############################
# Scheme-related Exceptions #
#############################


class SchemeError(Exception):
    """
    A type of exception to be raised if there is an error with a Scheme
    program.  Should never be raised directly; rather, subclasses should be
    raised.
    """

    pass


class SchemeSyntaxError(SchemeError):
    """
    Exception to be raised when trying to evaluate a malformed expression.
    """

    pass


class SchemeNameError(SchemeError):
    """
    Exception to be raised when looking up a name that has not been defined.
    """

    pass


class SchemeEvaluationError(SchemeError):
    """
    Exception to be raised if there is an error during evaluation other than a
    SchemeNameError.
    """

    pass


############################
# Tokenization and Parsing #
############################


def number_or_symbol(value):
    """
    Helper function: given a string, convert it to an integer or a float if
    possible; otherwise, return the string itself

    >>> number_or_symbol('8')
    8
    >>> number_or_symbol('-5.32')
    -5.32
    >>> number_or_symbol('1.2.3.4')
    '1.2.3.4'
    >>> number_or_symbol('x')
    'x'
    """
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return value


def tokenize(source):
    """
    Splits an input string into meaningful tokens (left parens, right parens,
    other whitespace-separated values).  Returns a list of strings.

    Arguments:
        source (str): a string containing the source code of a Scheme
                      expression
    >>>tokenize("(cat (dog (tomato)))")

    """
    lines = [lines for lines in source.splitlines() if not lines.startswith(";")]

    new_lines = []
    for line in lines:
        new_line = []
        for string in line.split():
            if string != ";":
                new_line.append(string)
            else:
                new_lines.extend(new_line)
                continue
    if new_lines != []:
        new_source = "\n".join(new_lines)
    else:
        new_source = "\n".join(lines)

    new = new_source.replace("(", " ( ").replace(")", " ) ").split()
    return new


def parse(tokens):
    """
    Parses a list of tokens, constructing a representation where:
        * symbols are represented as Python strings
        * numbers are represented as Python ints or floats
        * S-expressions are represented as Python lists

    Arguments:
        tokens (list): a list of strings representing tokens
    """

    count_l = 0
    count_r = 0
    final = 0
    for index, par in enumerate(tokens):
        if par == "(":
            count_l += 1
        if par == ")":
            final = index
            count_r += 1

    if count_r != count_l:
        raise SchemeSyntaxError
    if len(tokens) > 1:
        if tokens[0] == ")" and tokens[1] == "(":
            raise SchemeSyntaxError
        if "(" not in tokens:
            raise SchemeSyntaxError
    if tokens[len(tokens) - 1] != tokens[final]:
        raise SchemeSyntaxError

    def parse_helper(index):
        if tokens[index] == "(":
            new_list = []
            while tokens[index + 1] != ")":
                exp = parse_helper(index + 1)
                new_list.append(exp[0])
                index = exp[1] - 1
            return new_list, index + 2

        else:
            v = number_or_symbol(tokens[index])
            return v, index + 1

    parsed_expression, next_index = parse_helper(0)

    return parsed_expression


######################
# Built-in Functions #
######################
Booleans=["#t","#f"]
def product(args):
    """returns product"""
    result = 1
    for val in args:
        result *= val
    return result


def divide(args):
    """return result of dividing"""
    result = args[0]
    for val in args[1:]:
        result /= val

    return result

def equal(args):
    first=args[0]
    for arg in args[1:]:
        if  first== arg:
            first=arg
            continue
        else:
            return Booleans[1]
    return Booleans[0]    

def greater(args):
    first=args[0]
    for arg in args[1:]:
        if  first> arg:
            first=arg
            continue
        else:
            return Booleans[1]
    return Booleans[0]

def non_inc(args):
    first=args[0]
    for arg in args[1:]:
        if  first>=arg:
            first=arg
            continue
        else:
            return Booleans[1]
    return Booleans[0]

def less(args):
    first=args[0]
    for arg in args[1:]:
        if  first< arg:
            first=arg
            continue
        else:
            return Booleans[1]
    return Booleans[0]
def non_dec(args):
    first=args[0]
    for arg in args[1:]:
        if  first<=arg:
            first=arg
            continue
        else:
            return Booleans[1]
    return Booleans[0]
def check_both(args,frame):
 
    for arg in args:
        
        if evaluate(arg,frame)==Booleans[0]:
            continue
        else:
           return Booleans[1]
    return Booleans[0]
    
   

def either(args,frame):
  
    for arg in args:
   
        if evaluate(arg,frame)==Booleans[0]:
            return Booleans[0]
        else:
            continue
    return Booleans[1]

def none(arg):
    if len([arg])>1 or len(arg)==0:
        raise SchemeEvaluationError
  
    if evaluate(arg)==Booleans[0]:
        return Booleans[1]
    else:
        return Booleans[0]
    
def car(object):
   
    if len(object)>1:
        raise SchemeEvaluationError
    if object==[]:
        raise SchemeEvaluationError
    # object=evaluate(object,frame)
    if isinstance(object[0],Pair):
    
        return object[0].car
    else:
        raise SchemeEvaluationError
def cdr(object):
    
    if len(object)>1:
        raise SchemeEvaluationError
    if object==[]:
        raise SchemeEvaluationError

    # object=evaluate(object,frame)
    if isinstance(object[0],Pair):
       
        return object[0].cdr
    else:
        raise SchemeEvaluationError
    
def cons(args):
      
        if len(args)!=2:
            raise SchemeEvaluationError
        else:
            car=args[0]
            cdr=args[1]
            return Pair(car,cdr)
   
def if_list(arg):
    """
    For an object to be a list the object has to have a nil
    """
    print(arg,'arg')
    if arg[0]==[]:
        return Booleans[0]
    if not isinstance(arg[0],Pair):
        return Booleans[1]
    else:
        return if_list([cdr(arg)])

def length(list):
    if list[0]==[]:
        return 0
    if not isinstance(list[0],Pair):
        raise SchemeEvaluationError
    else:
        return 1 + length([cdr(list)])

def list_ref(args):
    main=args[0]
    indx=args[1]

    if indx==0:
        return car([main])
    else:
        
        return list_ref([cdr([main]),indx-1])
    
# def helper(pair,result):
#     if cdr(pair)=='nil':
#         return result
#     else:

#         result=Pair()
    
    
def concat(args):
    ####how to convert it into a list
    # print('hey')
    # if args==[]:
    #     return []
    # # if not isinstance(args[0],Pair):
    # #     print('hi')
    # #     return SchemeEvaluationError
    # else:
        
    #     if len(args)==1:
    #         new=args[0]
    #         return new
    #     else:
    #         new_list=[]
    #         for ex in args:
    #             # print(ex,'ex',args)
    #             if ex==[]:
                
    #                 continue
    #             if not isinstance(ex,Pair):
    #                 # print(ex,'error')
    #                 return SchemeEvaluationError
              
    #             else:
    #                 sub_list=ex.get_list()
               
    #                 new_list.extend(sub_list)
            
             
    #         tree=['list']+new_list
    #         if evaluate(tree)==[]:
    #             print('me')
    #             return []
    #         else:
                
    #             return evaluate(tree)

    final=[]
    for pair in args:

   
        while cdr([pair])!='nil':
            result=Pair(car([pair]),'nil')
            val=car([pair])
            result=Pair(car([result]),val)
            pair=cdr([pair])
        final=Pair(result,'nil')
    return final
    
        

        
            
   
def map(tree):
    # print(tree)
    # if isinstance(tree[1],Pair):
    #     if tree[1]==[]:
    #         return []
    #     else:
    #         sub=tree[1].get_list()
    #         new_list=[]
    #         for val in sub:
    #             new_list.append(tree[0]([val]))
    #         return evaluate(['list']+new_list)
    # else:
    #     if tree[1]==[]:
    #         return []
    #     else:
    #         raise SchemeEvaluationError
    print(tree[1])
    if isinstance(tree[1],Pair):
        arg=tree[1]
        func=tree[0]
        new_arg=[]
        new_arg=Pair(func([car([arg])]),'nil')
        arg=cdr([arg])
        while cdr([arg])!='nil':
            
            new_val=func([car([arg])])
            print(new_val)
            new_arg=Pair(car([new_arg]),new_val)
            print(car([new_arg]))
            arg=cdr([arg])
        return new_arg
    else:
        if tree[1]==[]:
            return []
        else:
            raise SchemeEvaluationError
        
        
def filter(tree,frame):
    if isinstance(tree[1],Pair):
        if tree[1]==[]:
            return []
        else:
            sub=tree[1].get_list()
            new_list=[]
            for val in sub:
                if tree[0]([val])==Booleans[0]:
                    new_list.append(val)
            return evaluate(['list']+new_list,frame)
    else:
        if tree[1]==[]:
            return []
        else:
            raise SchemeEvaluationError
        
def reduce(tree):
    if isinstance(tree[1],Pair):
        if tree[1]==[]:
            return []
        else:
            func=tree[0]
            sub=tree[1].get_list()
            result=func([sub[0],tree[2]])
            for val in sub[1:]:

                result=func([val,result])
                print(result,val)
            return result
    else:
        if tree[1]==[]:
            return []
        else:
            raise SchemeEvaluationError
            
        


    
    
scheme_builtins = {
    "+": sum,
    "-": lambda args: -args[0] if len(args) == 1 else (args[0] - sum(args[1:])),
    "*": product,
    "/": divide,
    'equal?':equal,
    '>': greater,
    '>=' : non_inc,
    '<=':non_dec,
    '<':less,
    'nil':[],
    'not':none,
    '#t': Booleans[0],
    '#f': Booleans[1],
    'car': car,
    'cdr': cdr,
    'cons': cons,
    'list?': if_list,
    'length':length,
    'list-ref':list_ref,
    'append': concat,
    'map':map,
    'reduce':reduce,
    
}


##############
# Evaluation #
##############
class Frames:
    """class for all frames created"""

    def __init__(self, parent, variables=None):

        self.variables = {}
        self.parent = parent

    def set(self, key, value):

        self.variables[key] = value

        return value

    def get_variable(self, name):
        if name in self.variables:
            # if self.variables[name] in self.variables:

            #     return self.variables[self.variables[name]]
            # else:

                return self.variables[name]
        else:

            while self.parent is not None:

                return self.parent.get_variable(name)
            raise SchemeNameError (f'{name}')


class Functions:
    """handles functions"""

    def __init__(self, frame, body, names):
        self.body = body
        self.names = names
        self.frame = frame

    def __call__(self, args):
   
        func_frame = Frames(self.frame)
        if len(self.names) != len(args):

            raise SchemeEvaluationError
        for name, val in zip(self.names, args):
            func_frame.set(name, val)
        return evaluate(self.body, func_frame)


builtins = Frames(None)
for key, val in scheme_builtins.items():
    builtins.set(key, val)

class Pair:
    def __init__(self,car,cdr):
        self.car=car
        self.cdr=cdr

    def get_list(self):
        if self.cdr==[]:
            return [self.car]
        if isinstance(self.cdr,(int,float)):
            return [self.car]+[self.cdr]
        else:
            return [self.car] + self.cdr.get_list()


        
    # def create_list(self,args):
    #     for arg in args:



def evaluate(tree, frame=None):
    """
    Evaluate the given syntax tree according to the rules of the Scheme
    language.

    Arguments:
        tree (type varies): a fully parsed expression, as the output from the
                            parse function
    """
   
    if frame == None:

        frame = Frames(builtins)

    if isinstance(tree, str):

        return frame.get_variable(tree)

    if isinstance(tree, (float, int)):

        return tree
    
    if tree==[]:
        raise SchemeEvaluationError

    if isinstance(tree, list):  # list (might be define...)

        if tree[0] == "define":
            if isinstance(tree[1], list):
                if len(tree[1]) > 1:
                    new_tree = ["lambda", tree[1][1:], tree[2]]
                    return frame.set(tree[1][0], evaluate(new_tree, frame))
                else:
                    new_tree = ["lambda", [], tree[2]]
                    return frame.set(tree[1][0], evaluate(new_tree, frame))

            else:

                result = evaluate(tree[2], frame)
                return frame.set(tree[1], result)

        if tree[0] == "lambda":
            body = tree[2]
            names = tree[1]
            frame = frame
            return Functions(frame, body, names)
        
       

        
        if tree[0]=='if':
            if tree[1] in Booleans:
               
                pred=tree[1]
            else:
                pred=evaluate(tree[1],frame)
                
            if pred==Booleans[0]:

                return evaluate(tree[2],frame)
            else:
                return evaluate(tree[3],frame)
        
        
        
            
        if tree[0]=='list':
            
            if len(tree)==1:
                return evaluate('nil',frame)
            else:
                extra=['list']
                if len(tree)>2:
                    extra.extend(tree[2:])
                new_tree=['cons',tree[1],extra]
               
                return evaluate(new_tree,frame)
            
        if tree[0]=='filter':
            args = [evaluate(name, frame) for name in tree[1:]]
            return filter(args,frame)
              

         

        if tree[0]=='and':
            return check_both(tree[1:],frame)
        if tree[0]=='or':
            return either(tree[1:],frame)
        #if tree[0]==let, translate it into a lambdaho
       
        else:
            func = evaluate(tree[0], frame)
           

            if callable(func):
                args = [evaluate(name, frame) for name in tree[1:]]
              
                return func(args)
            else:
                if func in Booleans:
                    return func
                else:
                    print(tree,'hey')
                    raise SchemeEvaluationError

    else:
        raise SchemeEvaluationError


def result_and_frame(tree, frame=None):

    if frame == None:

        frame = Frames(builtins)
    result = evaluate(tree, frame)

    return result, frame


def repl(verbose=False):
    """
    Read in a single line of user input, evaluate the expression, and print
    out the result. Repeat until user inputs "QUIT"

    Arguments:
        verbose: optional argument, if True will display tokens and parsed
            expression in addition to more detailed error output.
    """
    import traceback

    _, frame = result_and_frame(["+"])  # make a global frame
    while True:
        input_str = input("in> ")
        if input_str == "QUIT":
            return
        try:
            token_list = tokenize(input_str)
            if verbose:
                print("tokens>", token_list)
            expression = parse(token_list)
            if verbose:
                print("expression>", expression)
            output, frame = result_and_frame(expression, frame)
            print("  out>", output)
        except SchemeError as e:
            if verbose:
                traceback.print_tb(e.__traceback__)
            print("Error>", repr(e))


if __name__ == "__main__":
    # code in this block will only be executed if lab.py is the main file being
    # run (not when this module is imported)

    # uncommenting the following line will run doctests from above
    # doctest.testmod()
    # source=';add the numbers 2 and 3\n (+ ; this expression\n 2 ; 
    # spans multiple\n 3  ; lines\n spam)'
    # print(tokenize(source))\
    # print(parse(['(', '+', '2', '(', '-', '5', '3', ')', '7', '8', ')']))
    repl()
   
