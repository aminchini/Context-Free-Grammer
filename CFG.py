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
                if type(rule) == list and len(rule) == 2 and any([i.islower() or not i.isalpha() for i in rule]):
                    form1 = False
        return form1 and form2

    def check_if_greibach(self):
        result = True
        for rules in self.cfg.values():
            counter = 0
            for rule in rules:
                if type(rule) == list:
                    if rule[0].islower() or not rule[0].isalpha():
                        for i in rule[1::]:
                            if i.islower() or not i.isalpha():
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
        else:
            return False

    '''---------------------------------------------------------------------------------------------'''
    '''ChangeToGreibachForm'''
    def ChangeToGreibachForm(self):
        cfg_copy = self.DeleteTrash()
        keys = list(cfg_copy.keys())
        for key in keys:
            for des in cfg_copy[key]:
                if type(des) == list:
                    if des[0].islower() or not des[0].isalpha():
                        new_des = list()
                        f_item = des.pop(0)
                        new_des.append(f_item)
                        for item in des:
                            if item.isupper():
                                new_des.append(item)
                            else:
                                cfg_copy["T'"+item.upper()] = [item]
                                new_des.append("T'"+item.upper())
                        cfg_copy[key].remove(des)
                        cfg_copy[key].append(new_des)
                    elif all([i.isupper() for i in des]):
                        var = des.pop(0)
                        for item in cfg_copy[var]:
                            new_des = list()
                            new_des.append(item)
                            new_des += des
                            cfg_copy[key].append(new_des)

                        cfg_copy[key].remove(des)
                    elif des[0] == key and (des[1].islower() or not des[1].isalpha()):
                        beta = list()
                        alpha = list()
                        cfg_cc = copy.deepcopy(cfg_copy[key])
                        for item in cfg_cc:
                            if type(item) != list:
                                beta.append(item)
                            elif item[0] == key and (item[1].islower() or not item[1].isalpha()):
                                alpha.append(item[1])
                                cfg_copy[key].remove(item)
                        for b in beta:
                            cfg_copy[key].append([b, key+"'"])
                        cfg_copy[key+"'"] = list()
                        for a in alpha:
                            cfg_copy[key+"'"].append([a, key+"'"])
                    else:
                        new_deses = list()
                        f_item = des.pop(0)
                        for terms in cfg_copy[f_item]:
                            new_deses.append([terms])
                        variables = list()
                        for item in des:
                            if item.isupper():
                                variables.append(item)
                            else:
                                cfg_copy["T'"+item.upper()] = [item]
                                variables.append("T'"+item.upper())
                        for arr in new_deses:
                            cfg_copy[key].append(arr + variables)
                            
                        cfg_copy[key].remove(des)

        return cfg_copy

    '''---------------------------------------------------------------------------------------------'''
    '''ChangeToChomskyForm'''
    def ChangeToChomskyForm(self):
        cfg_copy = self.DeleteTrash()
        v_counter = 0
        v_checking = dict()
        keys = list(cfg_copy.keys())
        result = dict()
        for key in keys:
            result[key] = list()
            for des in cfg_copy[key]:
                if type(des) == list:
                    temp = list()
                    for item in des:
                        if item.isupper():
                            temp.append(item)
                        else:
                            result["T'"+item.upper()] = [item]
                            temp.append("T'"+item.upper())
                    while len(temp) > 2:
                        var1 = temp.pop()
                        var2 = temp.pop()
                        checking_key = var1+var1
                        if checking_key not in v_checking.keys():
                            v_index = 'V'+str(v_counter)
                            result[v_index] = [[var2, var1]]
                            v_checking[checking_key] = v_index
                            v_counter += 1
                            temp.append(v_index)
                        else:
                            v_index = v_checking[checking_key]
                            temp.append(v_index)
                            
                    result[key].append(temp)
                else:
                    result[key].append(des)
                    
        return result

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
            cfg = copy.deepcopy(cfg_copy)
            for key in cfg_copy.keys():
                for des in cfg[key]:
                    if type(des) == list and len(des) == 1:
                        units.append((key, des[0]))
                        cfg_copy[key].remove(des)
            return units

        units = unit_finder()
        while units:
            unit = units.pop()
            if unit[0] == unit[1]:
                continue
            if unit[0] == self.start_var or len(cfg_copy[unit[0]]):
                for item in cfg_copy[unit[1]]:
                    cfg_copy[unit[0]].append(item)
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
    def IsGenerateByGrammer(self, string: str):
        string = string.split()
        cfg_chomsky = self.ChangeToChomskyForm()
        r_dict = dict()
        r = 0
        for key in cfg_chomsky.keys():
            r_dict[key] = r
            r += 1
        
        R = dict()
        c = 1
        for key in cfg_chomsky.keys():
            R[c] = key
            c += 1

        s_dict = dict()
        n = 1
        for st in string:
            s_dict[n] = st
            n += 1

        cyk = dict()
        for i in range(1, n):
            d1 = dict()
            for j in range(1, n):
                d2 = dict()
                for k in range(1, c):
                    d2[k] = False
                d1[j] = d2
            cyk[i] = d1

        for i in range(1, n):
            for j in range(1, c):
                for terminals in cfg_chomsky[R[j]]:
                    if terminals == s_dict[i]:
                        cyk[1][i][j] = True

        for i in range(2, n):
            for j in range(1, n-i+1):
                for k in range(1, i):
                    for key in cfg_chomsky.keys():
                        for des in cfg_chomsky[key]:
                            if type(des) == list:
                                a = r_dict[key] + 1
                                b = r_dict[des[0]] + 1
                                c = r_dict[des[1]] + 1
                                if cyk[k][j][b] and cyk[i-k][j+k][c]:
                                    cyk[i][j][a] = True
        return cyk[n-1][1][1]


    '''---------------------------------------------------------------------------------------------'''
    def __str__(self):
        return str([self.cfg, self.start_var, self.isChomskyForm, self.isGreibachNormalForm, self.isDeleteTrash])
