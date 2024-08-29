import numbers
import re

from tokenize import Double


opstack = []  #assuming top of the stack is the end of the list

# Dictionary operations
def opPop():
    if opstack.__len__() == 0:
        return None
    return opstack.pop()
    # opPop should return the popped value.
    # The pop() function should call opPop to pop the top value from the opstack, but it will ignore the popped value.

def opPush(value):
    opstack.append(value)


dictstack = []  #assuming top of the stack is the end of the list


def dictPop():
    dictstack.pop()
    # dictPop pops the top dictionary from the dictionary stack.

def dictPush(d):
    dictstack.append(d)
    #dictPush pushes the dictionary ‘d’ to the dictstack.

def define(name, value):
    if dictstack.__len__() == 0:
        dictPush([(name, value)])
    else:
        for index, entry in enumerate(dictstack[-1]):
            if isinstance(entry, tuple):
                if name == entry[0]:
                    y = list(entry)
                    y[1] = value
                    x = tuple(y)
                    dictstack[-1][index] = x
                    return
        dictstack[-1].append((name, value))

def lookup(name):
    newName = '/' + name
    try:
        for dic in reversed(dictstack):   
            for item in dic:
                if isinstance(item, tuple):
                    if newName == item[0]:
                        return item[1]
                elif isinstance(item, dict):
                    for item2 in item:
                        if isinstance(item2, tuple):
                            if newName == item2[0]:
                                return item2[1]
    except:
        return "Not in stack"
    
# Arithmetic and comparison operators
def add():
    x1 = opPop()
    x2 = opPop()
    try:
        opPush(x1 + x2)
    except:
        opPush(x2)
        opPush(x1)
        return '(notanum)'

def sub():
    x1 = opPop()
    x2 = opPop()
    try:
        opPush(x2 - x1)
    except:
        return 'The variable is not a number'

def mul():
    x1 = opPop()
    x2 = opPop()
    try:
        opPush(x1 * x2)
    except:
        return 'The variable is not a number'

def div():
    x1 = opPop()
    x2 = opPop()
    try:
        opPush(x2 / x1)
    except:
        return 'The variable is not a number'

def mod():
    x1 = opPop()
    x2 = opPop()
    try:
        opPush(x2 % x1)
    except:
        return 'The variable is not a number'

def eq():
    x1 = opPop()
    x2 = opPop()
    try:
        opPush(x1 == x2)
    except:
        return 'The variable is not a number'

def lt():
    x1 = opPop()
    x2 = opPop()
    try:
        opPush(x1 > x2)
    except:
        return 'The variable is not a number'

def gt():
    x1 = opPop()
    x2 = opPop()
    try:
        opPush(x1 < x2)
    except:
        return 'The variable is not a number'

# String operators
def length():
    str1 = opPop()
    try:
        opPush(str1.__len__())
    except:
        return 'The op is not a string'

def get():
    i = opPop()
    str1 = opPop()
    try:
        opPush(ord(str1[i+1]))
    except:
        return 'The op is not a string'

def getinterval():
    count = opPop()
    start = opPop()
    str1 = opPop()
    try:
        ans = str1[(start + 1):(start + count + 1)]
        opPush(ans)
    except:
        return 'The op is not a string'

def put():
    val = opPop()
    i = opPop()
    str1 = opPop()
    strID = id(str1)
    try:
        tgt = str1[i]
        #newStr = str1.replace(tgt, chr(val), 1)
        newStr = str1[:i + 1] + chr(val) + str1[i + 2:]
        
        for idx, itm in enumerate(dictstack):
            if id(itm[1]) == strID:
                y = list(itm)
                y[1] = newStr
                x = tuple(y)
                dictstack[idx] = x # your new tuple
                
        for idx, itm in enumerate(opstack):
            if id(itm) == strID:
                opstack[idx] = newStr # your new tuple
    except:
        return 'The op is not a string'

# Manipulation and print operators

def dup():
    try:
        val = opPop()
        opPush(val)
        opPush(val)
    except:
        return 'Not enough operators'

def copy():
    try:
        for item in opstack:
            opPush(item)
    except:
        return 'Not enough operators'

def pop():
    try:
        opPop()
    except:
        return 'Not enough operators'

def clear():
    try:
        while opstack.__len__():
            pop()
    except:
        return 'Not enough operators'

def exch():
    try:
        val1 = opPop()
        val2 = opPop()
        opPush(val1)
        opPush(val2)
    except:
        return 'Not enough operators'

def roll():
    try:
        i = opPop()
        i2 = 0
        n = opPop()
        if i < 0:
            i *= -1
            n = opstack.__len__() - n
            while i2 < i:
                item = opstack[n]
                del opstack[n]
                opstack.append(item)
                i2 += 1
        else:
            n %= opstack.__len__()
            while i2 < i:
                item = opPop()
                opstack.insert(n, item)
                i2 += 1
        
        
    except:
        return 'Not enough operators'

def stack():
    try:
        for item in reversed(opstack):
            print(item)
    except:
        return 'Not enough operators'

# Dictionary manipulation operators
def psDict():
    try:
        size = opPop()
        opPush([])
    except:
        return 'stack error'

def begin():
    try:
        d = opPop()
        dictPush(d)
    except:
        return 'Stack error'

def end():
    dictPop()

def psDef():
    try:
        val = opPop()
        name = opPop()
        define(name, val)
    except:
        return 'Def error'

def tokenize(s):
    return re.findall("/?[a-zA-Z()][a-zA-Z0-9_()]*|[-]?[0-9]+|[}{]+|%.*|[^ \t\n]", s)

# The sequence of return characters represent a list of properly nested
# tokens, where the tokens between '{' and '}' is included as a sublist. If the
# parenteses in the input iterator is not properly nested, returns False.
def groupMatching2(it):
    res = []
    for c in it:
        if c == '}':
            return res
        elif c=='{':
            res.append(groupMatching2(it))
        else:
            if isnum(c):
                res.append(int(c))
            elif c == "true":
                res.append(True)
            elif c == "false":
                res.append(False)
            elif c == "[":
                arr = []
                while c in it != "]": # assumes there's a closing ]
                    arr.append(c)
                res.append(arr)
            else:
                res.append(c)
    return False


# Function to parse a list of tokens and arrange the tokens between { and } braces
# as code-arrays.
# Properly nested parentheses are arranged into a list of properly nested lists.
def parse(L):
    res = []
    it = iter(L)
    for c in it:
        if c=='}':
            return False
        elif c=='{':
            res.append(groupMatching2(it))
        else:
            if isnum(c):
                res.append(int(c))
            elif c == "true":
                res.append(True)
            elif c == "false":
                res.append(False)
            elif c == "[":
                arr = []
                while c in it != "]": # assumes there's a closing ]
                    arr.append(c)
                res.append(arr)
            else:
                res.append(c)
    return res


def isnum(s):
    try:
        float(s)
    except:
        return(False)
    else:
        return(True)

def interpretSPS(code): # code is a code array
    for tok in code:
         match tok:
            case "add":
                add()
            case "sub":
                sub()
            case "mul":
                mul()
            case "div":
                div()
            case "mod":
                mod()
            case "lt":
                lt()
            case "gt":
                gt()
            case "eq":
                eq()
            case "length":
                length()
            case "get":
                get()
            case "getinterval":
                getinterval()
            case "put":
                put()
            case "dup":
                dup()
            case "copy":
                copy()
            case "pop":
                pop()
            case "clear":
                clear()
            case "exch":
                exch()
            case "roll":
                roll()
            case "stack":
                stack()
            case "begin":
                begin()
            case "end":
                dictPop()
            case "def":
                psDef()
            case "dict":
                psDict()
            case "stack":
                stack()
            case "for": # push loop index to stack each iteration
                body = opPop()
                final = opPop()
                incr = opPop()
                init = opPop()
                
                for x in range(init, final - 1, incr):
                    opPush(x) # might have to flip order
                    interpretSPS(body)
            case "if":
                codeArr = opPop()
                test = opPop()
                if test:
                    interpretSPS(codeArr)
            case "ifelse":
                codeArr2 = opPop()
                codeArr1 = opPop()
                test1 = opPop()
                if test1:
                    interpretSPS(codeArr1)
                else:
                    interpretSPS(codeArr2)
            case _:
                # not hasattr(tok, "__len__") and not isinstance(tok, numbers.Number)
                if isinstance(tok, str):
                    ret = lookup(tok)
                    if ret == None:
                        opPush(tok)
                    else:
                        if isinstance(ret, list):
                            interpretSPS(ret)
                        else:
                            opPush(ret) # push value for variable
                else:
                    opPush(tok)


def interpreter(s): # s is a string
    interpretSPS(parse(tokenize(s)))


#clear opstack and dictstack
def clear():
    del opstack[:]
    del dictstack[:]


#testing

input1 = """
        /square {
               dup mul
        } def
        (square)
        4 square
        dup 16 eq
        {(pass)} {(fail)} ifelse
        stack
        """

input2 ="""
    (facto) dup length /n exch def
    /fact {
        0 dict begin
           /n exch def
           n 2 lt
           { 1}
           {n 1 sub fact n mul }
           ifelse
        end
    } def
    n fact stack
    """

input3 = """
        /fact{
        0 dict
                begin
                        /n exch def
                        1
                        n -1 1 {mul} for
                end
        } def
        6
        fact
        stack
    """

input4 = """
        /lt6 { 6 lt } def
        1 2 3 4 5 6 4 -3 roll
        dup dup lt6 {mul mul mul} if
        stack
        clear
    """

input5 = """
        (CptS355_HW5) 4 3 getinterval
        (355) eq
        {(You_are_in_CptS355)} if
         stack
        """

input6 = """
        /pow2 {/n exch def
               (pow2_of_n_is) dup 8 n 48 add put
                1 n -1 1 {pop 2 mul} for
              } def
        (Calculating_pow2_of_9) dup 20 get 48 sub pow2
        stack
        """


end = False
print("type \"end\" to end program")
clear

while(not end):
    uInput = input()
    if (uInput == "end"):
        end = True
    else:
        interpreter(uInput)
