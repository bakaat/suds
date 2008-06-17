# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
# written by: Jeff Ortel ( jortel@redhat.com )

"""
The I{sudsobject} module provides a collection of suds objects
that are primarily used for the highly dynamic interactions with
wsdl/xsd defined types.
"""

from suds import *
from new import classobj, function, instancemethod

log = logger(__name__)


def items(sobject):
    """
    Extract the I{items} from a suds object much like the
    items() method works on I{dict}.
    @param sobject: A suds object
    @type sobject: L{Object}
    @return: A list of items contained in I{sobject}.
    @rtype: [(key, value),...]
    """
    for k in sobject:
        yield (k, sobject[k])


def asdict(sobject):
    """
    Convert a sudsobject into a dictionary.
    @param sobject: A suds object
    @type sobject: L{Object}
    @return: A python dictionary containing the
        items contained in I{sobject}.
    @rtype: dict
    """
    return dict(items(sobject))


class Factory:
    
    @classmethod
    def subclass(cls, name, super):
        name = name.encode('utf-8')
        myclass = classobj(name,(super,),{})
        init = '__init__'
        src = 'def %s(self):\n' % init
        src += '\t%s.%s(self)\n' % (super.__name__,init)
        code = compile(src, '', 'exec')
        code = code.co_consts[0]
        fn = function(code, globals())
        m =  instancemethod(fn, None, myclass)
        setattr(myclass, name, m)
        return myclass
    
    @classmethod
    def object(cls, classname=None, dict={}):
        if classname is not None:
            subclass = cls.subclass(classname, Object)
            inst = subclass()
        else:
            inst = Object()
        for a in dict.items():
            setattr(inst, a[0], a[1])
        return inst
    
    @classmethod
    def metadata(cls):
        return Metadata()
    
    @classmethod
    def property(cls, name, value=None):
        subclass = cls.subclass(name, Property)
        return subclass(value)


class Object:

    def __init__(self):
        self.__keylist__ = []
        self.__printer__ = Printer()
        self.__metadata__ = Metadata()

    def __setattr__(self, name, value):
        builtin =  name.startswith('__') and name.endswith('__')
        if not builtin and \
            name not in self.__keylist__:
            self.__keylist__.append(name)
        self.__dict__[name] = value
        
    def __getitem__(self, name):
        return getattr(self, name)
        
    def __iter__(self):
        return iter(self.__keylist__)

    def __len__(self):
        return len(self.__keylist__)
    
    def __contains__(self, name):
        return name in self.__keylist__
    
    def __repr__(self):
        return str(self)

    def __str__(self):
        return unicode(self).encode('utf-8')
    
    def __unicode__(self):
        return self.__printer__.tostr(self)
    
    
class Metadata(Object):
    def __init__(self):
        self.__keylist__ = []
        self.__printer__ = Printer()
        
        
class Property(Object):

    def __init__(self, value):
        Object.__init__(self)
        self.value = value
        
    def items(self):
        for item in items(self):
            if item[0] != 'value':
                yield item
        
    def get(self):
        return self.value
    
    def set(self, value):
        self.value = value
        return self


class Printer:
    """ 
    Pretty printing of a Object object.
    """
    
    def __init__(self):
        self.indent = (lambda n :  '%*s'%(n*3,' '))
    
    def tostr(self, object, indent=-2):
        """ get s string representation of object """
        return self.process(object, indent)
    
    def process(self, object, n=0, nl=False):
        """ print object using the specified indent (n) and newline (nl). """
        if object is None:
            return 'None'
        if self.complex(object):
            if isinstance(object, (Object, dict)):
                return self.print_complex(object, n+2, nl)
            if isinstance(object, (list,tuple)):
                return self.print_collection(object, n+2)
        if isinstance(object, Property):
            return self.print_property(object)
        if isinstance(object, Object):
            object = asdict(object)
        if isinstance(object, (dict,list,tuple)):
            if len(object) > 0:
                return tostr(object)
            else:
                return '<empty>'
        return '(%s)' % tostr(object)
    
    def print_property(self, d):
        """ print a property object """
        s = []
        cls = d.__class__
        s.append('property:')
        s.append(cls.__name__)
        s.append('=')
        s.append(self.process(d.value))
        return ''.join(s)
    
    def print_complex(self, d, n, nl=False):
        """ print complex using the specified indent (n) and newline (nl). """
        s = []
        if nl:
            s.append('\n')
            s.append(self.indent(n))
        if isinstance(d, Object):
            cls = d.__class__
            if cls != Object:
                s.append('(')
                s.append(cls.__name__)
                s.append(')')
        s.append('{')
        for item in items(d):
            s.append('\n')
            s.append(self.indent(n+1))
            if isinstance(item[1], (list,tuple)):            
                s.append(item[0])
                s.append('[]')
            else:
                s.append(item[0])
            s.append(' = ')
            s.append(self.process(item[1], n, True))
        s.append('\n')
        s.append(self.indent(n))
        s.append('}')
        return ''.join(s)

    def print_collection(self, c, n):
        """ print collection using the specified indent (n) and newline (nl). """
        s = []
        for item in c:
            s.append('\n')
            s.append(self.indent(n))
            s.append(self.process(item, n-2))
            s.append(',')
        return ''.join(s)
    
    def complex(self, object):
        """ get whether the object is a complex type """
        if isinstance(object, (Object, dict)):
            if len(object) > 1:
                return True
            for item in items(object):
                if self.complex(item[1]):
                    return True
        if isinstance(object, (list,tuple)):
            if len(object) > 1: return True
            for c in object:
                if self.complex(c):
                    return True
            return False
        return False