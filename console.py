#!/usr/bin/python3
""" module cnsole airbnb"""

import cmd
import sys
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models import storage

class HBNBCommand(cmd.Cmd):
    """line-oriented command interpreters"""

    if sys.stdin and sys.stdin.isatty():
        prompt = "(hbnb) "
    else:
        prompt = "(hbnb) \n"

    def emptyline(self):
        """ return empty line"""
        pass

    """def default(self, line):
        invalid command message
        self.stdout.write('[-] Unknown command: %s' % (line,))"""

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """ Quit command to exit the program """
        return True

    def precmd(self, args):
        """ before the command line line is interpreted """
        if (args[-6:] == ".all()"):
            args = "all " + args[:-6]
        if (args[-8:] == ".count()"):
            args = "count " + args[:-8]
        if (args.find(".show(") != -1):
            args = "show " + ((args.replace(".show(", " "))[:-1])
            args = args.replace('"', "")
        if (args.find(".destroy(") != -1):
            args = "destroy " + ((args.replace(".destroy(", " "))[:-1])
            args = args.replace('"', "")
        if (args.find(".update(") != -1):
            if (args.find("{") == -1):
                """ si no me pasan un dict """
                args = "update " + ((args.replace(".update(", " "))[:-1])
                args = args.replace(",", "")
                args = args.replace('"', "")
            else:
                """ si me pasan un dict """
                idx = args.find("{")
                dic = (args[idx:-1])
                args = "update " + args[:idx]
                args = args.replace(".update(", " ")
                args = args.replace(",", "")
                args = args.replace('"', "")
                args = args + dic
        return args

    def do_create(self, args):
        """ Creates a new instance of BaseModel """
        if len(args) == 0:
            print("** class name missing **")
            return
        try:
            new_class = eval(args)()
            new_class.save()
            print(new_class.id)
        except Exception:
            print("** class doesn't exist **")

    def do_show(self, args):
        """ Prints the string representation of an instance """
        if len(args) == 0:
            print("** class name missing **")
            return
        tokens = args.split()

        if tokens[0] not in storage.all_class():
            print("** class doesn't exist **")
            return

        if len(tokens) < 2:
            print("** instance id missing **")
            return
        key = str(tokens[0]) + '.' + str(tokens[1])
        objects = storage.all()

        try:
            print(objects[key])
        except Exception:
            print("** no instance found **")

    def do_destroy(self, args):
        """ Deletes an instance based on the class name """
        if len(args) == 0:
            print("** class name missing **")
            return
        tokens = args.split()

        if tokens[0] not in storage.all_class():
            print("** class doesn't exist **")
            return

        if len(tokens) < 2:
            print("** instance id missing **")
            return
        key = str(tokens[0]) + '.' + str(tokens[1])
        objects = storage.all()

        if key in objects:
            storage.delete(key)
            storage.save()
        else:
            print("** no instance found **")

    def do_all(self, args):
        """ Prints all string representation """
        tokens = args.split()
        objects = storage.all()

        if len(tokens) > 0:
            if tokens[0] not in storage.all_class():
                print("** class doesn't exist **")
                return
            my_list = []
            for key, value in objects.items():
                if tokens[0] == value.__class__.__name__:
                    my_list.append(str(value))
            print(my_list)
        else:
            my_list = []
            for key, value in objects.items():
                my_list.append(str(value))
            print(my_list)

    def do_count(elf, args):
        """ returns number of instances """
        tokens = args.split()
        objects = storage.all()
        if len(tokens) == 1:
            if tokens[0] not in storage.all_class():
                print("** class doesn't exist **")
            else:
                count = 0
                for k, v in objects.items():
                    if (v.__class__.__name__ == tokens[0]):
                        count += 1
                print(count)

    def do_update(self, args):
        """ Updates an instance based on the class name   """

        if len(args) == 0:
            print("** class name missing **")
            return

        tokens = args.split()
        if tokens[0] not in storage.all_class():
            print("** class doesn't exist **")
            return

        if len(tokens) < 2:
            print("** instance id missing **")
            return

        key = str(tokens[0]) + '.' + str(tokens[1])
        objects = storage.all()

        if key not in objects:
            print("** no instance found **")
            return

        if len(tokens) < 3:
            print("** attribute name missing **")
            return
        if tokens[2].find("{") == -1:
            if len(tokens) < 4:
                print("** value missing **")
                return

            if tokens[3][0] == '"':
                tokens[3] = tokens[3][1:]
            if tokens[3][-1] == '"':
                tokens[3] = tokens[3][:-1]
            setattr(objects[key], tokens[2], tokens[3])
        else:
            """ update w/ dictionary """
            lenght = len(tokens)
            dic = ""
            """ todos los tokens menos clase y id """
            for i in range(2, lenght):
                dic += tokens[i]
            """dic = eval(tokens[2])"""
            dic = eval(dic)
            storage.set_atr(key, dic)


if __name__ == '__main__':
    HBNBCommand().cmdloop()
    
