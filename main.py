from earthquakes_repo_tryout.earthquakes import get_earthquake

days = 2
mag, place = get_earthquake(days)

print("The largest earthquake of last {} days had magnitude {} and was located at {}".format(days, mag, place))

