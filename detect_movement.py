from correlate import *

def pravila(acc_data, times=[],
			duration=0.5, debug=False):
	ret = ''
	l = len(acc_data)
	if times != []:
		endT = times[-1]
		for i in range(l-a, -1, -1):
			if (endT - times[i]) > duration:
				startI = i
		else:
			startI = 0
	else:
		startI = 0
	if max(acc_data[0][startI:]) > 500:
		ret += 'dol '
	if min(acc_data[0][startI:]) < -500:
		ret += 'gor '
	if max(acc_data[2][startI:]) > 300:
		ret += 'ndesno '
	if min(acc_data[2][startI:]) < -500:
		ret += 'nlevo '
	if min(acc_data[0][startI:]) < -300 and \
		max(acc_data[0][startI:]) > 200 and \
		max(acc_data[2][startI:]) > 200:
		ret += 'obrat '
	ret = ret.strip()
	if not debug:
		return ret
	r2 = []
	for i in range(3):
		r2 += [min(acc_data[i][startI:])]
		r2 += [max(acc_data[i][startI:])]
	return ret, r2

def split_inputs(filename, sensor, splits):
	mmax = 500
	mmin = -500
	times, data = parse(filename, sensor)
	dt = (times[-1] - times[0])/len(times)
	for i in range(3):
		mmin = min(mmin, min(data[i]))
		mmax = max(mmax, max(data[i]))
	f, ax = plt.subplots(3, 1, sharex=True)#, sharey=True)
	for i in range(3):
		ax[i].plot(times, data[i], label=str(i))
		#odvod = np.gradient(data[i], dt)
		#ax[i].plot(times, odvod)
		for j in splits:
			pass
			#ax[i].plot([j, j], [mmin, mmax], 'r-')
	plt.xlim(min(times), max(times))
	#plt.ylim(mmin, mmax)
	f.set_size_inches(11, 5)
	plt.savefig('head_movement_grafi/' + 
		filename.split('/')[1].split('.')[0] +'.png',
		bbox_inches='tight', dpi=300)



if __name__ == "__main__":
	sensor = '/muse/acc'
	files = 'dol.csv gor.csv nagib-levo.csv nagib-desno.csv\
			 obrat-desno.csv obrat-levo.csv'.split()
	for i in range(len(files)):
		files[i] = 'data/' + files[i]
		split_inputs(files[i], sensor, [2])
