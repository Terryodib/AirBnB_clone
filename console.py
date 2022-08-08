#!/usr/bin/python3
'''Code for HBNB console, commands, and options'''

from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
import models
import cmd


class HBNBCommand(cmd.Cmd):
    '''class that holds commands and options for HBNBCommand'''
    prompt = '(hbnb) '

    classes = {
        "BaseModel": BaseModel,
        "User": User,
        "City": City,
        "State": State,
        "Amenity": Amenity,
        "Place": Place,
        "Review": Review
    }

    def emptyline(self):
        '''Catches emptyline to not run anything'''
        pass

    # ----- basic commands -----
    def do_quit(self, arg):
        '''Quit command to exit the program'''
        return True

    def do_EOF(self, arg):
        '''EOF command to exit the program'''
        print('')
        return True

    # ----- view instances -----
    def do_show(self, arg):
        '''show, prints string representation\
of a instance based on class name and id'''
        arg = arg.split()
        if len(arg) < 1:  # class name exist?
            print("** class name missing **")
            return
        if arg[0] not in self.classes:  # class exist?
            print("** class doesn't exist **")
            return
        elif len(arg) < 2:  # id arg exist?
            print("** instance id missing **")
            return
        argument = arg[0] + "." + arg[1]  # class.id
        if argument not in models.storage.all():  # object exist storage?
            print("** no instance found **")
            return
        else:
            obj = models.storage.all()[argument]  # __objects.all()[User.'id']
            print(obj)

    def do_all(self, arg):
        '''all, prints string representation\
of all instances based or not on class name'''
        arg = arg.split()
        if arg:  # all <classname> OR all
            if arg[0] not in self.classes:  # class exist?
                print("** class doesn't exist **")
                return
            else:
                for inst in models.storage.all().keys():
                    instan = inst.split('.')
                    if instan[0] == arg[0]:
                        print(models.storage.all()[inst])
        else:
            # print all instances
            for inst in models.storage.all().keys():
                print(models.storage.all()[inst])

    # ----- manage instances -----
    def do_create(self, arg):
        '''create, creates new instance of <classname> and prints id\
e.x. "create User"'''
        arg = arg.split()
        if len(arg) < 1:  # class name exist?
            print("** class name missing **")
            return
        elif arg[0] not in self.classes:  # class exist?
            print("** class doesn't exist **")
            return
        else:
            new = self.classes[arg[0]]()
            new.save()
            print(new.id)

    def do_destroy(self, arg):
        '''destroy, deletes instance based on class name and id'''
        arg = arg.split()
        if len(arg) < 1:  # class name exist?
            print("** class name missing **")
            return
        if arg[0] not in self.classes:  # class exist?
            print("** class doesn't exist **")
            return
        elif len(arg) < 2:  # id arg exist?
            print("** instance id missing **")
            return
        argument = arg[0] + "." + arg[1]  # class.id
        if argument not in models.storage.all():  # object exist storage?
            print("** no instance found **")
            return
        else:
            models.storage.all().pop(argument)
            models.storage.save()

    def do_update(self, arg):
        '''update, updates an instance based on class name and id by\
 adding or updating attribute.\nex: update <classname> <id> <key> <value>'''
        arg = arg.split()
        if len(arg) < 1:  # class name exist?
            print("** class name missing **")
            return
        if arg[0] not in self.classes:  # class exist?
            print("** class doesn't exist **")
            return
        elif len(arg) < 2:  # id arg exist?
            print("** instance id missing **")
            return
        argument = arg[0] + "." + arg[1]  # class.id
        if argument not in models.storage.all():  # object exist storage?
            print("** no instance found **")
            return
        elif len(arg) < 3:  # attr arg exist?
            print("** attribute name missing **")
            return
        elif len(arg) < 4:  # val arg exist?
            print("** value missing **")
            return
        else:
            obj = models.storage.all()[argument]  # __objects.all()[User.'id']
            if arg[2] in obj.to_dict():  # get instance from spec. inst
                setattr(obj, arg[2], type(getattr(obj, arg[2]))(arg[3]))
            else:
                setattr(obj, arg[2], arg[3])
            obj.save()

if __name__ == "__main__":
    HBNBCommand().cmdloop()
