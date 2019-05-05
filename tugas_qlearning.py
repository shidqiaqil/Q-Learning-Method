reward=0
alpha=0.01
beta=13
r=[]
qsa=[]
start=210
finish=14
episode=5000
action='a'
#Membuka file
with open('DataTugas3ML2019.txt') as fp:
	for line in fp:
		x=[]
		for el in line.split():
			x.append(int(el))
		r.append(x)

#membuat Tabel QSA
qsa=([[0 for j in range(4)] for i in range(len(r)*len(r[0]))])

#mengubah array menjadi kolom
def nomor_kolom(a):
	return a%15

#memngubah array menjadi baris
def nomor_baris(a):
	return a//15

#mendapatkan reward disetiap kotak
def get_reward(a):
	return r[nomor_baris(a)][nomor_kolom(a)]

#menentukan arah	
def next(a,b):
	if b == 'a':
		return a-15
	elif b == 'b':
		return a+1
	elif b == 'c':
		return a+15
	elif b == 'd':
		return a-1

#pengecekan posisi
def atas(a):
	return (not nomor_baris(a))
def kiri(a):
	return (not nomor_kolom(a))
def kanan(a):
	return nomor_kolom(a) == 14
def bawah(a):
	return nomor_baris(a) == 14
def ataskiri(a):
	return atas(a) and kiri(a)
def bawahkiri(a):
	return bawah(a) and kiri(a)
def bawahkanan(a):
	return bawah(a) and kanan(a)

#update QSA
def updateqsa(a,b):
	return alpha*(get_reward(next(a,b)) + beta*max(qsa[next(a,b)]) + qsa[a][ord(b)-97])

#perulangan episode
while episode:
	now=start
	step=100
	while step:
		if ataskiri(now):
			x=[qsa[now][1],qsa[now][2]]
			ind=x.index(max(x))
			action=chr(ind+98)
		elif atas(now):
			x=[qsa[now][1],qsa[now][2],qsa[now][3]]
			ind=x.index(max(x))
			action=chr(ind+98)
		elif bawahkiri(now):
			x=[qsa[now][0],qsa[now][1]]
			ind=x.index(max(x))
			action=chr(ind+97)
		elif bawahkanan(now):
			x=[qsa[now][3],qsa[now][0]]
			ind=x.index(max(x))
			action=chr(((ind+3)%4)+97)
		elif bawah(now):
			x=[qsa[now][3],qsa[now][0],qsa[now][1]]
			ind=x.index(max(x))
			action=chr(((ind+3)%4)+97)
		elif kiri(now):
			x=[qsa[now][0],qsa[now][1],qsa[now][2]]
			ind=x.index(max(x))
			action=chr(ind+97)
		elif kanan(now):
			x=[qsa[now][2],qsa[now][3],qsa[now][0]]
			ind=x.index(max(x))
			action=chr(((ind+2)%4)+97)
		else:
			x=qsa[now]
			ind=x.index(max(x))
			action=chr(ind+97)
		qsa[now][ord(action)-97]+=updateqsa(now,action)
		step-=1
		now=next(now,action)
		if now==finish:
			step=0
	episode-=1
now=start

while now != finish:
	prev=now
	if not nomor_baris(now):
		if not nomor_kolom(now):
			x=[qsa[now][1],qsa[now][2]]
			ind=x.index(max(x))
			now=next(now,chr(ind+98))
		else:
			x=[qsa[now][1],qsa[now][2],qsa[now][3]]
			ind=x.index(max(x))
			now=next(now,chr(ind+98))
	elif nomor_baris(now) == 14:
		if not nomor_kolom(now):
			x=[qsa[now][0],qsa[now][1]]
			ind=x.index(max(x))
			now=next(now,chr(ind+97))
		elif nomor_kolom(now) == 14:
			x=[qsa[now][0],qsa[now][3]]
			ind=x.index(max(x))
			if not ind:
				now=next(now,'a')
			else:
				now=next(now,'d')
		else:
			x=[qsa[now][0],qsa[now][1],qsa[now][3]]
			ind=x.index(max(x))
			if not ind:
				now=next(now,'a')
			elif ind == 1:
				now=next(now,'b')
			else:
				now=next(now,'d')
	elif not nomor_kolom(now):
		x=[qsa[now][0],qsa[now][1],qsa[now][2]]
		ind=x.index(max(x))
		now=next(now,chr(ind+97))
	elif nomor_kolom(now) == 14:
		x=[qsa[now][0],qsa[now][2],qsa[now][3]]
		ind=x.index(max(x))
		if not ind:
			now=next(now,'a')
		elif ind == 1:
			now=next(now,'c')
		else:
			now=next(now,'d')
	else:
		x=qsa[now]
		ind=x.index(max(x))
		now=next(now,chr(ind+97))
	reward+=r[nomor_baris(now)][nomor_kolom(now)]
	gap=prev-now
	action="atas" if gap==15 else "kanan"
	print("dari [",(15-nomor_baris(prev)),"][",(nomor_kolom(prev)+1),"] aksi : ",action," ke [",(15-nomor_baris(now)),"][",(nomor_kolom(now)+1),"] reward = ",reward)