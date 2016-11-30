similarArtists <- artist.getSimilar("Imagine Dragons")$name[1:10]
dat <- data.frame(similarArtists)
names(dat)[1] <- "Artist"
#art <- NA
#trackInfo <- NA
artistTopTracks <- list()
art <- data.frame(artistTopTracks)
for(i in 1:10) {
  artistTopTracks <- artist.getTopTracks(dat[i,])$track
  art[i] <- data.frame(artistTopTracks)
  names(art)[i] <- similarArtists[i]
#  for (j in 1:10){
 #trackInfo[i][j] <- data.frame(track.getInfo(track=artistTopTracks[j], artist=similarArtists[i]))    
#  }
}
#art <- data.frame(artistTopTracks)
View(artistTopTracks)
