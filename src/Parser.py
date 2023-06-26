from Lexer import *

class Query:
    def __init__(self):
        self.type = None
        self.projection = []
        self.tables = []

        # select, update, delete
        self.where1 = { 'col': (None, None), 'operator': None, 'val': None }
        self.whereConnective = None
        self.where2 = { 'col': (None, None), 'operator': None, 'val': None }

        # select
        self.joins = []
        self.order_by = { 'col1': (None, None), 'col2': (None, None), 'is_asc': True }

        # Update and Insert
        self.assignments = { 'cols': [], 'vals': [] }

class Parser:
    def __init__(self, sql_query):
        self.lx = Lexer(sql_query.lower());
        pass

    def parse(self):
        self.q = Query()

        curr_tk = self.lx.get_next()
        self.q.type = curr_tk

        if curr_tk == 'select':
            return self.parse_select()
        elif curr_tk == 'insert':
            return self.parse_insert()
        elif curr_tk == 'update':
            return self.parse_update()
        elif curr_tk == 'delete':
            return self.parse_delete()
        else:
            raise Exception('Parser invalid sql command: {}'.format(curr_tk));

    def parse_select(self):
        # Parse projection
        while self.lx.peek() != 'from':
            curr_tk = self.lx.get_next()
            if curr_tk == ',':
                pass
            else:
                col_list = curr_tk.split('.', 1)
                if len(col_list) == 1:
                    self.q.projection.append((None, col_list[0]))
                else:
                    self.q.projection.append((col_list[0], col_list[1]))

        # Parse from clause
        self.lx.get_next() # from
        while self.lx.peek() not in [None, 'join', 'where', 'order']:
            curr_tk = self.lx.get_next()
            if curr_tk == ',':
                pass
            else:
                self.q.tables.append(curr_tk)

        # Parse join clauses
        while self.lx.peek() == 'join':
            self.lx.get_next()

            join_table = self.lx.get_next()
            if self.lx.get_next() == 'on':
                col_list = self.lx.get_next().split('.', 1)
                first_col = (None, col_list[0]) if len(col_list) == 1 else (col_list[0], col_list[1])
                self.lx.get_next() # =
                col_list = self.lx.get_next().split('.', 1)
                second_col = (None, col_list[0]) if len(col_list) == 1 else (col_list[0], col_list[1])

            else: # using
                self.lx.get_next() # (
                first_col = second_col = (None, self.lx.get_next())
                self.lx.get_next() # )

            self.q.joins.append((join_table, first_col, second_col))

        # Parse where clause
        if self.lx.peek() == 'where':
            self.lx.get_next()
            self.parse_where_predicate()

        # Parse order by clause
        if self.lx.peek() == 'order':
            self.lx.get_next()
            if self.lx.get_next() != 'by':
                raise Exception('Expecting "by" after "order"')

            col_list = self.lx.get_next().split('.', 1)
            self.q.order_by['col1'] = (None, col_list[0]) if len(col_list) == 1 else (col_list[0], col_list[1])

            if self.lx.peek() == ',':
                self.lx.get_next()
                col_list = self.lx.get_next().split('.', 1)
                self.q.order_by['col2'] = (None, col_list[0]) if len(col_list) == 1 else (col_list[0], col_list[1])

            self.q.order_by['is_asc'] = self.lx.get_next() != 'desc'

        return self.q

    def parse_where_predicate(self):
        # Format: col1 = x AND/OR col2 = y

        col_list = self.lx.get_next().split('.', 1)
        self.q.where1['col'] = (None, col_list[0]) if len(col_list) == 1 else (col_list[0], col_list[1])
        self.q.where1['operator'] = self.lx.get_next()
        self.q.where1['val'] = self.lx.get_next()

        if self.lx.peek() in ['and', 'or']:
            self.q.whereConnective = self.lx.get_next()

            print(self.lx.peek())

            col_list = self.lx.get_next().split('.', 1)
            self.q.where2['col'] = (None, col_list[0]) if len(col_list) == 1 else (col_list[0], col_list[1])
            self.q.where2['operator'] = self.lx.get_next()
            self.q.where2['val'] = self.lx.get_next()

    def parse_insert(self):
        self.lx.get_next() # into
        self.q.tables.append(self.lx.get_next())
        self.lx.get_next() # (

        self.q.assignments['cols'].append(self.lx.get_next())
        
        while self.lx.peek() == ',':
            self.lx.get_next() # ,
            self.q.assignments['cols'].append(self.lx.get_next())

        self.lx.get_next() # )
        self.lx.get_next() # values
        self.lx.get_next() # (

        self.q.assignments['vals'].append(self.lx.get_next())
        while self.lx.peek() == ',':
            self.lx.get_next() # ,
            self.q.assignments['vals'].append(self.lx.get_next())

        self.lx.get_next() # )

        return self.q

    def parse_update(self):
        self.q.tables.append(self.lx.get_next())
        self.lx.get_next() # set

        self.q.assignments['cols'].append(self.lx.get_next())
        self.lx.get_next() # =
        self.q.assignments['vals'].append(self.lx.get_next())
        
        while self.lx.peek() == ',':
            self.lx.get_next() # ,
            self.q.assignments['cols'].append(self.lx.get_next())
            self.lx.get_next() # =
            self.q.assignments['vals'].append(self.lx.get_next())

        # Parse where clause
        if self.lx.peek() == 'where':
            self.lx.get_next()
            self.parse_where_predicate()

        return self.q


    def parse_delete(self):
        self.lx.get_next() # from
        self.q.tables.append(self.lx.get_next())

        # Parse where clause
        if self.lx.peek() == 'where':
            self.lx.get_next()
            self.parse_where_predicate()

        return self.q
