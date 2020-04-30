import numpy as np
from matplotlib.figure import Figure

#search is the resulting table from the query
def create_figure(search):
	n_groups = 7 #You can change the number of genres to display
	i=0
	count_buying,count_borrowing,count_exchanging=(),(),()
	total=[]
	genres=[]

	while(i<n_groups*4):
		if(search[i]['transaction_type']==1):
			count_exchanging = count_exchanging + (search[i]['Total_Books'],)
		elif(search[i]['transaction_type']==2):
			count_borrowing = count_borrowing + (search[i]['Total_Books'],)
		elif(search[i]['transaction_type']==3):
			count_buying = count_buying + (search[i]['Total_Books'],)

		elif(search[i]['transaction_type']==None):
			total.append(search[i]['Total_Books'])
			genres.append(search[i]['genre_name'] + "(" + str(search[i]['Total_Books']) + ")")
			if(len(count_exchanging)<len(genres)):
				count_exchanging = count_exchanging + (0,)
			if(len(count_borrowing)<len(genres)):
				count_borrowing = count_borrowing + (0,)
			if(len(count_buying)<len(genres)):
				count_buying = count_buying + (0,)
			if(len(genres)==n_groups):
				break

		i=i+1

	# count_exchanging = () + (1,) + (2,) + (3,) + (4,)
	# count_borrowing = (2,3,1,2)
	# count_buying = (2,3,1,1)
	# genres = ('A','B','C','D')

	fig = Figure()
	plt = fig.add_subplot(1, 1, 1)

	index = np.arange(n_groups)
	bar_width = 0.25
	opacity = 0.8

	rects1 = plt.bar(index, count_exchanging, bar_width,
	alpha=opacity,
	color='b',
	label='Exchanging')

	rects2 = plt.bar(index + bar_width, count_borrowing, bar_width,
	alpha=opacity,
	color='g',
	label='Borrowing')

	rects3 = plt.bar(index + (2*bar_width), count_buying, bar_width,
	alpha=opacity,
	color='r',
	label='Buying')

	plt.set_xlabel('Genres')
	plt.set_ylabel('Total_Books')
	# plt.xlabel('Person')
	# plt.ylabel('Scores')
	# plt.title('Scores by person')
	# plt.xticks(index + bar_width, ('A', 'B', 'C', 'D'))
	plt.set_xticks(index + bar_width)
	plt.set_xticklabels(tuple(genres))
	plt.legend()

	return fig
	