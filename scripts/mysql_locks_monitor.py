#!/usr/bin/env python
#coding:utf8


import MySQLdb



class op_mysql(object):


	def __init__(self,user,passwd,host,port,sql):
		self.user = user
		self.passwd = passwd
		self.host = host
		self.port = port
		self.sql = sql
		
	def conn_mysql(self):
		try:
			conn = MySQLdb.connect(host=self.host,port=self.port,user=self.user,passwd=self.passwd,connect_timeout=2)
			self.conn = conn
		except Exception as e:
			print(e)
			return "get conn faile"		

		try:
			self.cur = self.conn.cursor()
		except Exception as e:
			print(e)
			return "get cursor faile"		

	def select_mysql(self):
		self.cur.execute(self.sql)
		data = self.cur.fetchall()
		return data

	def change_mysql(self):
		try:
			self.cur.execute(self.sql)
			self.conn.commit()
			return "change is ok"
		except Exception as e:
			print("change msg: %s" % e)
			self.conn.rollback()


		

if __name__ == "__main__":
	
	conf = ['192.168.2.100:3308','','','']
	for line in conf:
		ip=line.split(":")[0]
		port = int(line.split(":")[1])
		print(ip,port)
		sql = "SELECT lw.requesting_trx_id AS request_ID,trx.trx_mysql_thread_id AS request_mysql_ID,trx.trx_query AS request_command,lw.blocking_trx_id AS blocking_ID,trx1.trx_mysql_thread_id AS blocking_mysql_ID,trx1.trx_query AS blocking_command,lo.lock_index AS lock_index FROM information_schema.innodb_lock_waits lw INNER JOIN information_schema.innodb_locks lo ON lw.requesting_trx_id = lo.lock_trx_id INNER JOIN information_schema.innodb_locks lo1 ON lw.blocking_trx_id = lo1.lock_trx_id INNER JOIN information_schema.innodb_trx trx ON lo.lock_trx_id = trx.trx_id INNER JOIN information_schema.innodb_trx trx1 ON lo1.lock_trx_id = trx1.trx_id"
		o = op_mysql(user="xxxx",passwd="xxxxxxxxxxxxxxxx",host=ip,port=port,sql=sql)
		o.conn_mysql()
		data = o.select_mysql()
		if data != ():
			requesting_trx_id = data[0][0]
			request_trx_mysql_thread_id = int(data[0][1])
			request_trx_query = data[0][2]
			blocking_trx_id = data[0][3]
			blocking_trx_mysql_thread_id = int(data[0][4])
			blocking_trx_query = data[0][5]
			lock_index = data[0][6]			
			id = 'NULL'
			host = ip
			port = int(port)
			c_t = 'UNIX_TIMESTAMP()'
			ins_sql = """insert into mysql_monitor.locks values (%s,%s,"%s",%s,%s,"%s","%s",%s,"%s",%s,%s)""" %(requesting_trx_id,request_trx_mysql_thread_id,request_trx_query,blocking_trx_id,blocking_trx_mysql_thread_id,blocking_trx_query,lock_index,id,host,port,c_t)
			print(ins_sql)
			ins = op_mysql(user="xxxxx",passwd="xxxxxxxxxxx",host='127.0.0.1',port=3306,sql=ins_sql)
			ins.conn_mysql()
			ins_data = ins.change_mysql()
			
"""

CREATE TABLE `locks` (
  `requesting_trx_id` varchar(18) NOT NULL DEFAULT '',
  `request_trx_mysql_thread_id` bigint(21) unsigned NOT NULL DEFAULT '0',
  `request_trx_query` varchar(1024) DEFAULT NULL,
  `blocking_trx_id` varchar(18) NOT NULL DEFAULT '',
  `blocking_trx_mysql_thread_id` bigint(21) unsigned NOT NULL DEFAULT '0',
  `blocking_trx_query` varchar(1024) DEFAULT NULL,
  `lock_index` varchar(1024) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `host` varchar(10) DEFAULT NULL,
  `port` int(11) DEFAULT NULL,
  `c_t` bigint(12) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8;


"""			
			
			
			
			
			
			