from GerenciadorArquivos import *
from Parser import *

class QueryProcessor:
    def __init__(self):
        self.ga = GerenciadorArquivos()

    def get_col_id_by_name(self, col_name, table):
        for i in range(0, len(table[0])):
            if (table[0][i].lower() == col_name):
                return i

    def get_proj_ids(self, projection, table):
        projection_ids = []

        if projection[0] == '*':
            for i in range(0, len(table[0])):
                projection_ids.append(i)
        else:
            for p in projection:
                for i in range(0, len(table[0])):
                    if (table[0][i].lower() == p):
                        projection_ids.append(i)
                        break
        return projection_ids

    def test_operator(self, col, op, val):
        val = int(val)
        col = int(col)
        if op == '=':
            return col == val
        elif op == '!=':
            return col != val
        elif op == '<':
            return col < val
        elif op == '>':
            return col > val
        elif op == '<=':
            return col <= val
        elif op == '>=':
            return col >= val
        return False

    def test_where(self, table, i, query):
        where1_res = False
        if query.where1['operator'] != None:
            col_id = self.get_col_id_by_name(query.where1['col'][1], table)
            if self.test_operator(table[i][col_id], query.where1['operator'], query.where1['val']):
                where1_res = True

        where2_res = False
        if query.where2['operator'] != None:
            col_id = self.get_col_id_by_name(query.where2['col'][1], table)
            if self.test_operator(table[i][col_id], query.where2['operator'], query.where2['val']):
                where2_res = True

        if query.whereConnective == None:
            if where1_res:
                return True
        elif query.whereConnective == 'and':
            if where1_res and where2_res:
                return True
        elif query.whereConnective == 'or':
            if where1_res or where2_res:
                return True
        return False

    def executeQuery(self, sql_command):
        p = Parser(sql_command)
        query = p.parse()

        if query.type == 'select':
            return self.execute_select(query)
        elif query.type == 'insert':
            return self.execute_insert(query)
        elif query.type == 'update':
            return self.execute_update(query)
        elif query.type == 'delete':
            return self.execute_delete(query)

    def join_tables(tableA, tableB, colA_id, colB_id):
        result = 

    def execute_select(self, query):
        table = self.ga.GETTABLE(query.tables[0])
        projection_ids = self.get_proj_ids(query.projection, table)

        if len(query.joins) > 0:

    def execute_insert(self, query):
        table = self.ga.GETTABLE(query.tables[0])
        projection_ids = self.get_proj_ids(query.assignments['cols'], table)

        new_line = [ None ] * len(table[0])
        for i in range(0, len(query.assignments['vals'])):
            new_line[projection_ids[i]] = query.assignments['vals'][i]

        table.append(new_line)
        self.ga.SAVETABLE(query.tables[0], table)

    def execute_update(self, query):
        table = self.ga.GETTABLE(query.tables[0])

        def exec_assigments(line_i):
            for i in range(0, len(query.assignments['cols'])):
                col_id = self.get_col_id_by_name(query.assignments['cols'][i], table)
                table[line_i][col_id] = query.assignments['vals'][i]

        for i in range(1, len(table)):
            if self.test_where(table, i, query):
                exec_assigments(i)

        self.ga.SAVETABLE(query.tables[0], table)

    def execute_delete(self, query):
        table = self.ga.GETTABLE(query.tables[0])
        to_pop = []

        for i in range(1, len(table)):
            if self.test_where(table, i, query):
                print(table[i])
                to_pop.append(i)

        print(len(to_pop))
        for i in reversed(to_pop):
            table.pop(i)
        self.ga.SAVETABLE(query.tables[0], table)
