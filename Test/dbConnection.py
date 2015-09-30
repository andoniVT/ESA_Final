#!/usr/bin/env python
# -*- coding: utf-8 -*- 
'''
Created on 20/3/2015

@author: ucsp
'''

# tablas: entidad - comentario

'''
 mysql --user=root -p
 alter table entidad AUTO_INCREMENT=1
'''

import MySQLdb

class Connection(object):
    
    def __init__(self):
        self.__server = "localhost"
        self.__user = "root"
        self.__pass = "jorgeandoni"
        #self.__pass = "bayern"
        #self.__db = "test"
        self.__db = "esa"
        self.__conn = MySQLdb.connect(self.__server, self.__user, self.__pass, self.__db)
    
    def test(self):
        c = self.__conn.cursor()
        c.execute("SELECT * FROM persona")
        rows = c.fetchall()
        for i in rows:
            print i
    
    def add_entity(self, nombre_entidad):
        c = self.__conn.cursor()
        consulta =  'SELECT * FROM entidad WHERE nombre="%s"' % (nombre_entidad,) + ";"        
        c.execute(consulta)
        rows = c.fetchall()
        if len(rows) == 0:
            consulta2 = 'INSERT INTO entidad VALUES (NULL, "%s")' % (nombre_entidad,) + ";"
            c.execute(consulta2)
            print consulta2
        else:
            print "Entidad " + nombre_entidad +  " ya existe!"
    
    def add_atributte(self, nombre_entidad, atributo, tipo):
        c = self.__conn.cursor()
        consulta = 'SELECT id_entidad FROM entidad WHERE nombre="%s"' %(nombre_entidad,) + ";"
        c.execute(consulta)
        rows = c.fetchall()
        if len(rows)!=0:            
            id_entidad = rows[0][0]
            consulta2 = ""
            if tipo == 1:
                consulta2 = 'INSERT INTO comentario VALUES (NULL, "%s"' % (atributo[0],) + ", " +'"%s"' % (atributo[1],) + ", " + str(id_entidad) + ");"
                
            else:
                consulta2 = 'INSERT INTO comentario2 VALUES (NULL, "%s"' % (atributo[0],) + ", " +  '"%s"' %(atributo[1],) + ", " + str(id_entidad) + ");"
                
            c.execute(consulta2)
            print consulta2
            
        else:
            print "Entidad " + nombre_entidad +  " no existe!"
    
    def get_polarity(self, nombre_entidad):
        positivos = 0
        negativos = 0
        neutros = 0
        c = self.__conn.cursor()
        consulta = 'SELECT * FROM entidad WHERE nombre="%s"' %(nombre_entidad,) + ";"
        c.execute(consulta)
        rows = c.fetchall()
        if len(rows)!= 0:
            consulta2 = 'select polaridad FROM entidad e, comentario2 c WHERE e.id_entidad=c.id_entidad AND e.nombre="%s"' % (nombre_entidad,) + ";"
            c.execute(consulta2)
            values = c.fetchall()
            for i in values:
                if i[0] == 0: neutros+=1
                if i[0] > 0: positivos+=1
                if i[0] < 0: negativos+=1                    
            #print consulta2
        else:
            print "Entidad " + nombre_entidad +  " no existe!"
        
        return [positivos,  neutros , negativos]          


if __name__ == '__main__':
    
    print "hello"
    
    con = Connection()
    con.add_entity("Movistar")
    #val = con.get_polarity("movistar")
    #print val 
    