class DoesNotExist(Exception):
	pass

class MultipleObjectsReturned(Exception):
	pass

class Student:
	def __init__(self, name, age, score):
		self.name = name
		self.student_id = None
		self.age = age
		self.score = score

	@staticmethod
	def get(student_id=0,name="",score=-1,age=0):
		if student_id != 0:
			record = read_data(f"select * from Student where student_id={student_id}")
		elif name != "":
			record = read_data(f"select * from Student where name={name}")
		elif score != -1:
			record = read_data(f"select * from Student where score={score}")
		elif age != 0:
			record = read_data(f"select * from Student where age={age}")
			
		if len(record)==0:
			raise DoesNotExist('DoesNotExist')
		elif len(record)>1:
			raise MultipleObjectsReturned('MultipleObjectsReturned')
		else:
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
			crsr.execute(f"update Student SET name={self.name},age={self.age},score={self.score}")
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

#student_obj = Student(name="rakesh1",age=22,score=87)
#student_obj.save()
#s=Student.delete()
#print(s)
#print(s.student_id)
#print(read_data("SELECT * FROM student"))
