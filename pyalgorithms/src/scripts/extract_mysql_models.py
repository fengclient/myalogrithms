'''
Create the web2py code needed to access your mysql legacy db.

To make this work all the legacy tables you want to access need to have an "id" field.

This plugin needs:
mysql
mysqldump
installed and globally available.

Under Windows you will probably need to add the mysql executable directory to the PATH variable,
you will also need to modify mysql to mysql.exe and mysqldump to mysqldump.exe below.
Just guessing here :)

Access your tables with:
legacy_db(legacy_db.mytable.id>0).select()

If the script crashes this is might be due to that fact that the data_type_map dictionary below is incomplete.
Please complete it, improve it and continue.

Created by Falko Krause, minor modifications by Massimo Di Pierro and Ron McOuat

2012-07-26: 
Changed by fengclient: 
1 force protocol=tcp on mysql and mysqldump
2 set DAL options
3 add primary key support
'''
import subprocess
import re
import sys
data_type_map = dict(
        varchar = 'string',
        int = 'integer',
        integer = 'integer',
        tinyint = 'integer',
        smallint = 'integer',
        mediumint = 'integer',
        bigint = 'integer',
        float = 'double',
        double = 'double',
        char = 'string',
        decimal = 'integer',
        date = 'date',
        #year = 'date',
        time = 'time',
        timestamp = 'datetime',
        datetime = 'datetime',
        binary = 'blob',
        blob = 'blob',
        tinyblob = 'blob',
        mediumblob = 'blob',
        longblob = 'blob',
        text = 'text',
        tinytext = 'text',
        mediumtext = 'text',
        longtext = 'text',
        )

def mysql(database_name, username, password):
    print 'from gluon.dal import DAL, Field'
    p = subprocess.Popen(['mysql',
                          '--protocol=tcp',
                          '--user=%s' % username,
                          '--password=%s'% password,
                          '--execute=show tables;',
                          database_name],
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    sql_showtables, stderr = p.communicate()
    tables = [re.sub('\|\s+([^\|*])\s+.*', '\1', x) for x in sql_showtables.split()[1:]]
    connection_string = "legacy_db = DAL('mysql://%s:%s@localhost/%s',pool_size=10, db_codec='latin1',migrate=False, migrate_enabled=False)"\
                        %(username, password, database_name)
    legacy_db_table_web2py_code = []
    for table_name in tables:
        #get the sql create statement
        p = subprocess.Popen(['mysqldump',
                              '--protocol=tcp',
                              '--user=%s' % username,
                              '--password=%s' % password,
                              '--skip-add-drop-table',
                              '--no-data', database_name,
                              table_name], stdin=subprocess.PIPE, stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        sql_create_stmnt,stderr = p.communicate()
        if 'CREATE' in sql_create_stmnt:#check if the table exists
            #remove garbage lines from sql statement
            sql_lines = sql_create_stmnt.split('\n')
            sql_lines = [x for x in sql_lines if not(x.startswith('--') or x.startswith('/*') or x =='')]
            #generate the web2py code from the create statement
            web2py_table_code = ''
            table_name = re.search('CREATE TABLE .(\S+). \(', sql_lines[0]).group(1)
            fields = []
            auto_increment_fields = []
            primary_key_fields = []
            id_field = None
            for line in sql_lines[1:-1]:
                hit_pk=re.search('PRIMARY KEY \((\S+)\)', line)
                if hit_pk:
                    primary_key_fields=re.findall('`(\S+?)`', line)
                if re.search('KEY', line) or re.search('PRIMARY', line) or re.search(' ID', line) or line.startswith(')'):
                    continue
                hit = re.search('(\S+)\s+(\S+)(,| )( .*)?', line)
                if hit!=None:
                    name, d_type = hit.group(1), hit.group(2)
                    d_type = re.sub(r'(\w+)\(.*',r'\1',d_type)
                    name = re.sub('`','',name)
                    if re.search('AUTO_INCREMENT',line):
                        auto_increment_fields.append(name)
                    fields.append((name,d_type))
            for (name, d_type) in fields:
                if name in primary_key_fields and name in auto_increment_fields and len(primary_key_fields)==1:
                    id_field = name
                    #i don't care d_type
                    web2py_table_code += "\n    Field('%s','%s'),"%(name,'id')
                else:
                    web2py_table_code += "\n    Field('%s','%s'),"%(name,data_type_map[d_type])
            if primary_key_fields:
                web2py_table_code += "\n    primarykey=[%s],"%(','.join(["'%s'"%(x) for x in primary_key_fields]))
            web2py_table_code = "legacy_db.define_table('%s',%s\n    migrate=False)"%(table_name,web2py_table_code)
            legacy_db_table_web2py_code.append(web2py_table_code)
    #----------------------------------------
    #write the legacy db to file
    legacy_db_web2py_code = connection_string+"\n\n"
    legacy_db_web2py_code += "\n\n#--------\n".join(legacy_db_table_web2py_code)
    return legacy_db_web2py_code

regex = re.compile('(.*?):(.*?)@(.*)')
if len(sys.argv)<2 or not regex.match(sys.argv[1]):
    print 'USAGE:\n\n    extract_mysql_models.py username:password@data_basename\n\n'
else:
    m = regex.match(sys.argv[1])
    print mysql(m.group(3),m.group(1),m.group(2))

