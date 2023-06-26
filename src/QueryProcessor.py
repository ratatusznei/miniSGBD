from GerenciadorArquivos import *
from Parser import *


def try_int(val):
    try:
        return int(val)
    except ValueError:
        return val


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
        if op == '=':
            return col.lower() == val
        elif op == '!=':
            return col.lower() != val
        elif op == '<':
            return try_int(col) < try_int(val)
        elif op == '>':
            return try_int(col) > try_int(val)
        elif op == '<=':
            return try_int(col) <= try_int(val)
        elif op == '>=':
            return try_int(col) >= try_int(val)
        return False

    def test_where(self, table, i, query):
        if query.where1['operator'] == None:
            return True

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

    def join_tables(self, tableA, tableB, colA_id, colB_id):
        result = [[]]
        for col in tableA[0]:
            result[0].append(col)
        colb_ids = []
        for i in range(0, len(tableB[0])):
            col = tableB[0][i]
            if col not in result[0]:
                result[0].append(col)
                colb_ids.append(i)

        for ai in range(1, len(tableA)):
            for bi in range(1, len(tableB)):
                if tableA[ai][colA_id] == tableB[bi][colB_id]:
                    new_line = []
                    for val in tableA[ai]:
                        new_line.append(val)
                    for i in colb_ids:
                        new_line.append(tableB[bi][i])

                    result.append(new_line)

        return result

    def execute_select(self, query):
        table = self.ga.GETTABLE(query.tables[0])

        join_res = table
        for j in query.joins:
            other_table = self.ga.GETTABLE(j[0])
            cola_id = self.get_col_id_by_name(j[1][1], join_res)
            colb_id = self.get_col_id_by_name(j[2][1], other_table)

            join_res = self.join_tables(join_res, other_table, cola_id, colb_id)


        where_res = [join_res[0]]
        for i in range(1, len(join_res)):
            if self.test_where(join_res, i, query):
                where_res.append(join_res[i])

        if query.order_by['col1'][1] != None:
            if query.order_by['col2'][1] != None:
                col1_id = self.get_col_id_by_name(query.order_by['col1'][1], where_res)
                col2_id = self.get_col_id_by_name(query.order_by['col2'][1], where_res)
                def my_key(e):
                    return (try_int(e[col1_id]), try_int(e[col2_id]))
            else:
                col1_id = self.get_col_id_by_name(query.order_by['col1'][1], where_res)
                def my_key(e):
                    return try_int(e[col1_id])

            col_names = where_res.pop(0)
            where_res.sort(reverse=not query.order_by['is_asc'], key=my_key)
            where_res.insert(0, col_names)


        if query.projection[0][1] != '*':
            proj_res = [[]]
            query.projection = list(map(lambda x: x[1], query.projection))
            projection_ids = self.get_proj_ids(query.projection, where_res)

            for pi in projection_ids:
                proj_res[0].append(where_res[0][pi])

            for i in range(1, len(where_res)):
                new_line = []
                for pi in projection_ids:
                    new_line.append(where_res[i][pi])
                proj_res.append(new_line)

            res = proj_res
        else:
            res = where_res

        # from pprint import pprint
        # pprint(res)

        return res

    def execute_insert(self, query):
        table = self.ga.GETTABLE(query.tables[0])
        projection_ids = self.get_proj_ids(query.assignments['cols'], table)

        new_line = [ None ] * len(table[0])
        for i in range(0, len(query.assignments['vals'])):
            new_line[projection_ids[i]] = query.assignments['vals'][i]

        table.append(new_line)
        self.ga.SAVETABLE(query.tables[0], table)
        return [ ['inseridos'], [1] ]

    def execute_update(self, query):
        table = self.ga.GETTABLE(query.tables[0])
        updated = 0

        def exec_assigments(line_i):
            for i in range(0, len(query.assignments['cols'])):
                col_id = self.get_col_id_by_name(query.assignments['cols'][i], table)
                table[line_i][col_id] = query.assignments['vals'][i]

        for i in range(1, len(table)):
            if self.test_where(table, i, query):
                exec_assigments(i)
                updated += 1

        self.ga.SAVETABLE(query.tables[0], table)
        return [ ['atualizados'], [updated] ]

    def execute_delete(self, query):
        table = self.ga.GETTABLE(query.tables[0])
        to_pop = []

        for i in range(1, len(table)):
            if self.test_where(table, i, query):
                to_pop.append(i)

        deleted = len(to_pop)
        for i in reversed(to_pop):
            table.pop(i)
        self.ga.SAVETABLE(query.tables[0], table)

        return [ ['deletados'], [deleted] ]
