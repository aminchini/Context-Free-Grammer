import re
import collections
import copy

class Grammer:
    '''Recieving Data'''
    def __init__ (self, input_data: list):
        self.var_num = int(input_data.pop(0))
        self.cfg = dict()
        for line in input_data:
            #It is very important to have space before and after '->' in input 
            rule = line.split(' -> ')
            items = rule[1].split('|')
            right = list()
            for item in items:
                if '<' in item and '>' in item:
                    temp = re.split('<|>', item)
                    right.append([i for i in temp if i != ''])
                else:
                    right.append(item)
            self.cfg[rule[0][1:-1:]] = right
        keys = list(self.cfg.keys())
        self.start_var = keys[0]
        self.isChomskyForm = self.check_if_chomsky()
        self.isGreibachNormalForm = self.check_if_greibach()
        self.isDeleteTrash = self.check_if_delete_trash()

    def check_if_chomsky(self):
        form1 = True
        form2 = True
        for rules in self.cfg.values():
            for rule in rules:
                if type(rule) == list and len(rule) != 2:
                    form1 = False
                if type(rule) == list and len(rule) == 2 and any([i.lower() for i in rule]):
                    form1 = False
        return form1 and form2

    def check_if_greibach(self):
        result = True
        for rules in self.cfg.values():
            counter = 0
            for rule in rules:
                if type(rule) == list:
                    if rule[0].islower():
                        for i in rule[1::]:
                            if i.islower():
                                result = False
                                break
                    else:
                        result = False
                        break
                else:
                    counter += 1
            if counter > 1:
                result = False
                break
            
        return result

    def check_if_delete_trash(self):
        compare = lambda x, y: collections.Counter(x) == collections.Counter(y)
        for rules in self.cfg.values():
            for rule in rules:
                # Nullable Variables checking
                if 'lamda' in rule:
                    return False
                # Unit-Productions checking
                if type(rule) == list:
                    if len(rule) == 1:
                        return False
        # Useless Productions checking
        terminal_reachable_variables = list()
        for key in self.cfg.keys():
            checker = False
            for des in self.cfg[key]:
                if type(des) != list:
                    checker = True
                    break
            if checker:
                terminal_reachable_variables.append(key)
        none_trv = [i for i in self.cfg.keys() if i not in terminal_reachable_variables]
        while True:
            copy_trv = copy.deepcopy(terminal_reachable_variables)
            for key in none_trv:
                for des in self.cfg[key]:
                    if type(des) == list:
                        temp = [i for i in des if i.isupper()]
                        if all(i in terminal_reachable_variables for i in temp) and key not in terminal_reachable_variables:
                            terminal_reachable_variables.append(key)
            if copy_trv == terminal_reachable_variables:
                break
        if compare(list(set(terminal_reachable_variables)), self.cfg.keys()):
            # Dependency Graph checking
            reachable_vars = list()
            reachable_vars.append(self.start_var)
            temp = list()
            temp.append(self.start_var)
            while temp:
                var = temp.pop()
                if var in self.cfg.keys():
                    for des in self.cfg[var]:
                        if type(des) == list:
                            for reach in des:
                                if reach.isupper() and reach not in reachable_vars:
                                    reachable_vars.append(reach)
                                    temp.append(reach)
                else:
                    continue
            if all([i in reachable_vars for i in self.cfg.keys()]):
                return True
        else:
            return False

    '''---------------------------------------------------------------------------------------------'''
    '''ChangeToGreibachForm'''
    def ChangeToGreibachForm(self):
        pass





    '''---------------------------------------------------------------------------------------------'''
    '''ChangeToChomskyForm'''
    def ChangeToChomskyForm(self):
        pass





    '''---------------------------------------------------------------------------------------------'''
    '''DeleteTrash'''
    def DeleteTrash(self):
        cfg_copy = copy.deepcopy(self.cfg)

        # Remove Nullable Variables
        null_vars = list()
        for key in self.cfg.keys():
            for des in self.cfg[key]:
                if des == 'lamda':
                    null_vars.append(key)
                    cfg_copy[key].remove('lamda')
        for null in null_vars:
            for key in self.cfg.keys():
                for des in self.cfg[key]:
                    if type(des) == list and null in des:
                        temp = [i for i in des if i != null]
                        if len(temp) != 0:
                            cfg_copy[key].append(temp)

       # Remove Unit-Productions
        def unit_finder():
            units = list()
            for key in cfg_copy.keys():
                for des in cfg_copy[key]:
                    if type(des) == list and len(des) == 1:
                        units.append((key, des[0]))
                        cfg_copy[key].remove(des)
            return units

        units = unit_finder()
        while units:
            unit = units.pop()
            if unit[0] == unit[1]:
                continue
            if unit[0] == self.start_var:
                for item in cfg_copy[unit[1]]:
                    cfg_copy[self.start_var].append(item)
                units += unit_finder()
            else:
                for key in cfg_copy.keys():
                    for des in cfg_copy[key]:
                        if type(des) == list and unit[0] in des:  
                            new_list = copy.deepcopy(des)
                            index = des.index(unit[0])
                            new_list[index] = unit[1]
                            cfg_copy[key].append(new_list)
                            units += unit_finder()
        empty_keys = list()
        for key in cfg_copy.keys():
            if len(cfg_copy[key]) == 0:
                empty_keys.append(key)
        for key in empty_keys:
            del cfg_copy[key]

        # Remove Useless Variables
        def delete_useless(vars):
            for item in vars:
                del cfg_copy[item]
                for key in cfg_copy.keys():
                    for des in cfg_copy[key]:
                        if type(des) == list and item in des:
                            cfg_copy[key].remove(des)

        def dependency_graph_remover():
            reachable_vars = list()
            reachable_vars.append(self.start_var)
            temp = list()
            temp.append(self.start_var)
            while temp:
                var = temp.pop()
                if var in cfg_copy.keys():
                    for des in cfg_copy[var]:
                        if type(des) == list:
                            for reach in des:
                                if reach.isupper() and reach not in reachable_vars:
                                    reachable_vars.append(reach)
                                    temp.append(reach)
                else:
                    continue
            if not all([i in reachable_vars for i in cfg_copy.keys()]):
                return [i for i in cfg_copy.keys() if i not in reachable_vars]
            else:
                return []

        should_be_deleted = list()
        compare = lambda x, y: collections.Counter(x) == collections.Counter(y)
        terminal_reachable_variables = list()
        for key in cfg_copy.keys():
            checker = False
            for des in cfg_copy[key]:
                if type(des) != list:
                    checker = True
                    break
            if checker:
                terminal_reachable_variables.append(key)
        none_trv = [i for i in cfg_copy.keys() if i not in terminal_reachable_variables]
        while True:
            copy_trv = copy.deepcopy(terminal_reachable_variables)
            for key in none_trv:
                for des in cfg_copy[key]:
                    if type(des) == list:
                        temp = [i for i in des if i.isupper()]
                        if all(i in terminal_reachable_variables for i in temp) and key not in terminal_reachable_variables:
                            terminal_reachable_variables.append(key)
            if copy_trv == terminal_reachable_variables:
                break
        if not compare(list(set(terminal_reachable_variables)), cfg_copy.keys()):
            should_be_deleted = [i for i in cfg_copy.keys() if i not in terminal_reachable_variables]
            delete_useless(should_be_deleted)
            should_be_deleted = dependency_graph_remover()
            delete_useless(should_be_deleted)
        else:
            should_be_deleted = dependency_graph_remover()
            delete_useless(should_be_deleted)
        return cfg_copy

    '''---------------------------------------------------------------------------------------------'''
    '''IsGenerateByGrammer'''
    def IsGenerateByGrammer(self):
        pass





    '''---------------------------------------------------------------------------------------------'''
    def __repr__(self):
        return str([self.cfg, self.isChomskyForm, self.isGreibachNormalForm, self.isDeleteTrash])



''''''''''''''''''''''''''''''''''''''
# G = Grammer([
#     5,
#     "<START> -> <SUBJECT><DISTANCE><VERB><DISTANCE><OBJECTS>",
#     "<SUBJECT> -> i|we",
#     "<DISTANCE> ->  ",
#     "<VERB> -> eat|drink|go|<OBJECTS><SUBJECT>",
#     "<OBJECTS> -> food|water|lamda"
# ])

G = Grammer([
    4,
    "<S> -> a<S>|<A>|<C>",
    "<A> -> a",
    "<B> -> aa",
    "<C> -> a<C>b",
])
print(G.DeleteTrash())
