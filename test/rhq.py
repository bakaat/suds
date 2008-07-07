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

#
# This test requires installation or visability to an RHQ server.
# ( http://www.rhq-project.org )
#

import sys
sys.path.append('../')

from suds import logger
import logging
from suds.client import Client

errors = 0
subject = None

#logger('suds.client').setLevel(logging.DEBUG)
#logger('suds.xsd.schema').setLevel(logging.DEBUG)

def start(url):
    global errors
    print '\n________________________________________________________________\n' 
    print 'Test @ ( %s )\nerrors = %d\n' % (url, errors)

def basic_doc_literal():
    
    global errors

    try:
        url = 'http://localhost:7080/rhq-rhq-enterprise-server-ejb3/WebServiceTestBean?wsdl'
        start(url)
        client = Client(url)
        #
        # create name
        #
        name = client.factory.create('name')
        name.first = u'jeff'+unichr(1234)
        name.last = 'ortel'
        #
        # create a phone object using the wsdl
        #
        phoneA = client.factory.create('phone')
        phoneA.npa = 410
        phoneA.nxx = 555
        phoneA.number = 5138
        phoneB = client.factory.create('phone')
        phoneB.npa = 919
        phoneB.nxx = 555
        phoneB.number = 4406
        #
        # create a person object using the wsdl
        #
        person = client.factory.create('person')
        print person
        person.name = name
        person.age = 43
        person.phone.append(phoneA)
        person.phone.append(phoneB)
        print person       
        #
        # addPerson()
        #
        print 'addPersion()'
        result = client.service.addPerson(person)
        print '\nreply(\n%s\n)\n' % str(result)
        #
        # create a new name object used to update the person
        #
        newname = client.factory.create('name')
        newname.first = 'Todd'
        newname.last = None
        #
        # update the person's name (using the webservice)
        #
        print 'updatePersion()'
        result = client.service.updatePerson(person, newname)
        print '\nreply(\n%s\n)\n' % str(result)
        result = client.service.updatePerson(person, None)
        print '\nreply(\n%s\n)\n' % str(result)
    except Exception, e:
        errors += 1
        print e
  
    try:
        print "echo('this is cool')"
        result = client.service.echo('this is cool')
        print '\nreply( %s )\n' % str(result)
        print 'echo(None)'
        result = client.service.echo(None)
        print '\nreply( %s )\n' % str(result)
    except Exception, e:
        errors += 1
        print e
        
    try:
        print 'hello()'
        result = client.service.hello()
        print '\nreply( %s )\n' % str(result)
    except Exception, e:
        errors += 1
        print e

    try:
        print 'testVoid()'
        result = client.service.testVoid()
        print '\nreply( %s )\n' % str(result)
    except Exception, e:
        errors += 1
        print e

    try:
        mylist = ['my', 'dog', 'likes', 'steak']
        print 'testListArgs(%s)' % mylist
        result = client.service.testListArg(mylist)
        print '\nreply( %s )\n' % str(result)
    except Exception, e:
        errors += 1
        print e
    
    try:
        s = 'hello'
        for n in range(0, 3):
            print 'getList(%s, %d)' % (s, n)
            result = client.service.getList(s, n)
            print '\nreply( %s )\n' % str(result)
            if len(result) != n:
                errors += 1
                print 'expected (%d), reply (%d)' % (n, len(result))
    except Exception, e:
        errors += 1
        print e
    
    try:
        print 'testExceptions()' 
        result = client.service.testExceptions()
        print '\nreply( %s )\n' % tostr(result)
        print 'Fault expected and not raised'
        errors += 1
    except Exception, e:
        print e
        
    #
    # test faults
    #
    try:
        url = 'http://localhost:7080/rhq-rhq-enterprise-server-ejb3/WebServiceTestBean?wsdl'
        start(url)
        client = Client(url, faults=False)
        print 'testExceptions()'
        result = client.service.testExceptions()
        print '\nreply( %s )\n' % str(result)
    except Exception, e:
        errors += 1
        print e
        
def basic_rpc_literal():
    
    global errors

    try:
        url = 'http://localhost:7080/rhq-rhq-enterprise-server-ejb3/WebServiceRPCTestBean?wsdl'
        start(url)
        client = Client(url)
        #
        # create name
        #
        name = client.factory.create('name')
        name.first = u'jeff'+unichr(1234)
        name.last = 'ortel'
        #
        # create a phone object using the wsdl
        #
        phoneA = client.factory.create('phone')
        phoneA.npa = 410
        phoneA.nxx = 555
        phoneA.number = 5138
        phoneB = client.factory.create('phone')
        phoneB.npa = 919
        phoneB.nxx = 555
        phoneB.number = 4406
        #
        # create a person object using the wsdl
        #
        person = client.factory.create('person')
        print person
        person.name = name
        person.age = 43
        person.phone.append(phoneA)
        person.phone.append(phoneB)
        print person       
        #
        # addPerson()
        #
        print 'addPersion()'
        result = client.service.addPerson(person)
        print '\nreply(\n%s\n)\n' % str(result)
        #
        # create a new name object used to update the person
        #
        newname = client.factory.create('name')
        newname.first = 'Todd'
        newname.last = None
        #
        # update the person's name (using the webservice)
        #
        print 'updatePersion()'
        result = client.service.updatePerson(person, newname)
        print '\nreply(\n%s\n)\n' % str(result)
        result = client.service.updatePerson(person, None)
        print '\nreply(\n%s\n)\n' % str(result)
    except Exception, e:
        errors += 1
        print e
  
    try:
        print "echo('this is cool')"
        result = client.service.echo('this is cool')
        print '\nreply( %s )\n' % str(result)
        print 'echo(None)'
        result = client.service.echo(None)
        print '\nreply( %s )\n' % str(result)
    except Exception, e:
        errors += 1
        print e
        
    try:
        print 'hello()'
        result = client.service.hello()
        print '\nreply( %s )\n' % str(result)
    except Exception, e:
        errors += 1
        print e

    try:
        print 'testVoid()'
        result = client.service.testVoid()
        print '\nreply( %s )\n' % str(result)
    except Exception, e:
        errors += 1
        print e

    try:
        array = client.factory.create('ns0:stringArray')
        array.item = ['my', 'dog', 'likes', 'steak']
        print 'testListArgs()\n%s\n' % array
        result = client.service.testListArg(array)
        print '\nreply( %s )\n' % str(result)
    except Exception, e:
        errors += 1
        print e
    
    try:
        s = 'hello'
        for n in range(0, 3):
            print 'getList(%s, %d)' % (s, n)
            result = client.service.getList(s, n)
            print '\nreply( %s )\n' % str(result)
            if n > 0 and n != len(result.item):
                errors += 1
                print 'expected (%d), reply (%d)' % (n, len(result.item))
    except Exception, e:
        errors += 1
        print e
    
    try:
        print 'testExceptions()' 
        result = client.service.testExceptions()
        print '\nreply( %s )\n' % tostr(result)
        print 'Fault expected and not raised'
        errors += 1
    except Exception, e:
        print e

    try:
        url = 'http://localhost:7080/rhq-rhq-enterprise-server-ejb3/WebServiceRPCTestBean?wsdl'
        start(url)
        client = Client(url, faults=False)
        print 'testExceptions()'
        result = client.service.testExceptions()
        print '\nreply( %s )\n' % str(result)
    except Exception, e:
        errors += 1
        print e
        
def authentication():
    
    global subject
    
    try:
        
        url = 'http://localhost:7080/rhq-rhq-enterprise-server-ejb3/SubjectManagerBean?wsdl'
        start(url)
        client = Client(url)
        print client
        #
        # login
        #
        print 'login()'
        subject = client.service.login('rhqadmin', 'rhqadmin')
        print '\nreply(\n%s\n)\n' % str(subject)
        #
        # create page control and get all subjects
        #
        pc = client.factory.create('pageControl')
        pc.pageNumber = 0
        pc.pageSize = 0
        #
        # getAllSubjects()
        #
        print 'getAllSubjects()'
        users = client.service.getAllSubjects(pc)
        print 'Reply:\n(\n%s\n)\n' % str(users)
        #
        # get user preferences
        #
        print 'loadUserConfiguration()'
        id = subject.id
        print subject
        prefs = client.service.loadUserConfiguration(id)
        print 'Reply:\n(\n%s\n)\n' % str(prefs)
    except Exception, e:
        errors += 1
        print e
        
def perspectives():
    
    global subject, errors
    
    try:
        url = 'http://localhost:7080/rhq-rhq-enterprise-server-ejb3/PerspectiveManagerBean?wsdl'
        start(url)
        client = Client(url)
        print client
        #
        # get all (content) perspectives
        #
        print 'getPerspective(content)'
        perspectives = client.service.getPerspective("content")
        print 'perspectives: ', str(perspectives)
        #
        # get all perspectives
        #     
        print 'getAllPerspective()'
        perspectives = client.service.getAllPerspectives()
        print 'perspectives: ', str(perspectives)
    except Exception, e:
        errors += 1
        print e
        
def content_source():
    
    global subject, errors
    
    try:
        url = 'http://localhost:7080/rhq-rhq-enterprise-server-ejb3/ContentSourceManagerBean?wsdl'
        start(url)
        client = Client(url)
        print client
        #
        # create a configuration
        #
        configuration = client.factory.create('configuration')
        entry = client.factory.create('configuration.tns:properties.tns:entry')
        simple = client.factory.create('propertySimple')
        entry.key = 'location'
        simple.name = 'location'
        simple.stringValue = 'http://download.skype.com/linux/repos/fedora/updates/i586'
        entry.value = simple
        configuration.properties.entry.append(entry)
        configuration.notes = 'SkipeAdapter'
        configuration.version = 1234
        print configuration
        #
        # create: name, description and type.
        #
        name = 'SkipeAdapter'
        description = 'The skipe adapter'
        type = 'YumSource'
        #
        # create a content source.
        #
        print 'createContentSource()'
        result = client.service.createContentSource(
                            subject, 
                            name, 
                            description, 
                            type, 
                            configuration, 
                            False)
        print 'createContentSource: ', str(result)
    except Exception, e:
        errors += 1
        print e

        
if __name__ == '__main__':
    
    errors = 0
    basic_doc_literal()
    basic_rpc_literal()
    authentication()
    perspectives()
    content_source()
    
    print '\nFinished: errors=%d' % errors