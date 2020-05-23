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
		
	def __repr__(self):
		return "Student(student_id={0}, name={1}, age={2}, score={3})".format(self.student_id,self.name,self.age,self.score)
	
	@classmethod
	def get(cls,**kwargs): 
		
		for key,value in kwargs.items():
			cls.column = key
			cls.value = value
	
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
	
	@staticmethod
	def filter(**args):
		final_outcome = []
		for k,v in args.items():
			invalid_field=k.split('__')
			if invalid_field[0] not in ('student_id','name','age','score'):
				raise InvalidField
			if k in ('student_id','name','age','score'):
				records = read_data(f"select * from Student where {k} = '{v}'")
			else:
				var = k.split('__')
				if var[1] == 'lt':
					records = read_data(f"select * from Student where {var[0]} < {v}")
				elif var[1] == 'lte':
					records = read_data(f"select * from Student where {var[0]} <= {v}")
				elif var[1] == 'gt':
					records = read_data(f"select * from Student where {var[0]} > {v}")
				elif var[1] == 'gte':
					records = read_data(f"select * from Student where {var[0]} >= {v}")
				elif var[1] == 'neq':
					records = read_data(f"select * from Student where {var[0]} <> '{v}'")
				elif var[1] == 'in':
					in_condition = tuple(v)
					records = read_data(f"select * from Student where {var[0]} in {in_condition}")
				elif var[1] == 'contains':
					records = read_data(f"select * from Student where {var[0]} LIKE '%{v}%'")
			
			for i in range(len(records)):
				output = Student(records[i][1],records[i][2],records[i][3])
				output.student_id = records[i][0]
				final_outcome.append(output)

		return final_outcome
			
	def save(self):
		import sqlite3
		connection = sqlite3.connect("selected_students.sqlite3")
		crsr = connection.cursor() 
		crsr.execute("PRAGMA foreign_keys=on;") 
		if self.student_id == None:
			crsr.execute(f"insert into Student (name,age,score) values (\'{self.name}\',{self.age},{self.score})")        
			self.student_id = crsr.lastrowid
		else:
			data = read_data(f"select * from  Student Where student_id={self.student_id}")
			if len(data) != 0:
				crsr.execute(f"update Student SET name=\'{self.name}\',age={self.age},score={self.score}")
			else:
				crsr.execute(f"insert into Student (student_id,name,age,score) values ({self.student_id},\'{self.name}\',{self.age},{self.score})")
		connection.commit() 
		connection.close()

	def delete(self):
		write_data(f"delete from student where student_id={self.student_id}")
		
	
def write_data(sql_query):
	import sqlite3
	connection = sqlite3.connect("selected_students.sqlite3")
	crsr = connection.cursor() 
	crsr.execute("PRAGMA foreign_keys=on;") 
	crsr.execute(sql_query) 
	connection.commit() 
	connection.close()

def read_data(sql_query):
	import sqlite3
	connection = sqlite3.connect("selected_students.sqlite3")
	crsr = connection.cursor()
	crsr.execute(sql_query) 
	ans= crsr.fetchall()  
	connection.close() 
	return ans
	
#print(read_data("select * from Student"))
#ages = [25,30]
#selected_students = Student.filter(name='mahi')
#print(selected_students)
