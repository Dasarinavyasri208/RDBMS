class DoesNotExist(Exception):
	pass

class MultipleObjectsReturned(Exception):
	pass

class InvalidField(Exception):
	pass

class Student:
	def __init__(self, name, age, score):
		self.name = name
		self.student_id = None
		self.age = age
		self.score = score

	@classmethod
	def get(cls,**kwargs): 
		
		for k,v in kwargs.items():
			cls.column = k
			cls.value = v
	
		if cls.column not in ('student_id','name','age','score'):
			raise InvalidField('InvalidField')
			
		if cls.column == 'name':
			record = read_data(f"select * from Student where {cls.column} = \'{cls.value}\'")
		else:
			record = read_data(f"select * from Student where {cls.column} = {cls.value}")
		
		if len(record)==0:
			raise DoesNotExist('DoesNotExist')
		elif len(record)>1:
			raise MultipleObjectsReturned('MultipleObjectsReturned')
	
		output = Student(record[0][1],record[0][2],record[0][3])
		output.student_id = record[0][0]
		return output

	def save(self):
		import sqlite3
		connection = sqlite3.connect("students.sqlite3")
		crsr = connection.cursor() 
		crsr.execute("PRAGMA foreign_keys=on;") 
		if self.student_id == None:
			crsr.execute(f"insert into Student (name,age,score) values (\'{self.name}\',{self.age},{self.score})")        
			self.student_id = crsr.lastrowid
		else:
			crsr.execute(f"update Student SET name=\'{self.name}\',age={self.age},score={self.score}")
		connection.commit() 
		connection.close()

	def delete(self):
		write_data(f"delete from student where student_id={self.student_id}")
	
def write_data(sql_query):
	import sqlite3
	connection = sqlite3.connect("students.sqlite3")
	crsr = connection.cursor() 
	crsr.execute("PRAGMA foreign_keys=on;") 
	crsr.execute(sql_query) 
	connection.commit() 
	connection.close()

def read_data(sql_query):
	import sqlite3
	connection = sqlite3.connect("students.sqlite3")
	crsr = connection.cursor()
	crsr.execute(sql_query) 
	ans= crsr.fetchall()  
	connection.close() 
	return ans

#student_obj = Student.get(rank=4)
#student_obj.name = "mahesh"
#student_obj.save()
#s=Student.delete()
#print(s)
#print(s.student_id)
#print(read_data("SELECT * FROM student"))
#(**args)
#rank=4
#dct = {'name':'a','age':0,'score':0}
