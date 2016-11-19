#Read .mp3 files from a given directory, compare songs, and play them in order of similarity

library("plyr")
library("tuneR")
library("seewave")

library("compiler")

library("foreach")
library("doParallel")
registerDoParallel()

orderSongs <- function(x, indexHlp = 1)
{
  sList <-cbind(as.data.frame(x), isIn = rep(0, times = nrow(x)))
  pList <- c()
  
  repeat{
    i <- indexHlp[1]
    indexHlp <- indexHlp[-1]
    
    pList <- c(pList, sList$V1[i], sList$V2[i])
    sList$isIn[i] <- 1
    
    if (length(which(sList$isIn == 0)) == 0 )
      break
    
    hlp1 <- which(sList$V1 == i & sList$isIn == 0)
    hlp2 <- which(sList$V2 == i & sList$isIn == 0)
    hlp3 <- as.numeric(rownames(sList[sList$isIn == 1 & (sList$V1 > 0 | sList$V2 > 0),]))
    
    if(sList$V1[i] > 0 & sList$V2[i] > 0){
      indexHlp <- c(indexHlp,  setdiff(c(sList$V2[i],sList$V1[i]), hlp3))
    }else if (length(hlp1) > 0 | length(hlp2) > 0){
      indexHlp <- c(indexHlp, min(hlp1, hlp2))
    }else{
      indexHlp <- c(indexHlp, max(setdiff(c(sList$V1[i], sList$V2[i]), hlp3)))}  
    
    if ((sList$V1[i] > 0) & (sList$V2[i] > 0) & ((length(hlp1) > 0) | (length(hlp2) > 0)))
      indexHlp <- c(indexHlp, min(hlp1, hlp2))
    
    indexHlp <- indexHlp[indexHlp > 0]  
  }
  
  -1*pList[pList < 0]
}

arrangeMusic <- function(inDirectory, startWith = NULL)
{
  #Get a list of .mp3 files from a given directory and read them in
  mList <- list.files(path = inDirectory, pattern = ".mp3")
  S <- alply(mList, 1, function(x) readMP3(x))

  print("Reading and processing songs... Depending on the number of the songs, this part may take a few minutes...")
  #Calculate the frequency spectra
  #This takes some time, so I will parallelize it
  
  fa <- foreach(i = 1:length(S)) %dopar% {ama(S[i], plot = FALSE)}
  
  #Next, I am going to compare frequency spectra distribution by computing different distance
  #Distances are not symetrical, e.g. dS1S2 != dS2S1, so I need to calculate all vs. all similarities 
  #(dSiSi is always equal to 0, so I could also exclude those)
  simTab <- data.frame(V1 = rep(1:length(mList), times = length(mList)), V2 = rep(1:length(mList), each = length(mList)))
  distS <- ddply(simTab, c("V1", "V2"), function(x) data.frame(IT = itakura.dist(fa[[x$V1]], fa[[x$V2]])$D1, KL = kl.dist(fa[[x$V1]], fa[[x$V2]])$D1, KS = ks.dist(fa[[x$V1]], fa[[x$V2]],f = 44100)$D, LS  = logspec.dist(fa[[x$V1]], fa[[x$V2]])))
  
  #Put the average distances in the matrix
  #But first normalize each of them
  simS <- matrix(nrow = length(S), ncol=length(S), dimnames = list(mList, mList))
  for (i in 1:nrow(distS))
    simS[distS$V1[i], distS$V2[i]] <- (distS$IT[i]/max(distS$IT) + distS$KL[i]/max(distS$KL) + distS$KS[i]/max(distS$KS) + distS$LS[i]/max(distS$LS))/4
  
  #Now calculate distances between songs, using the default parametes
  d <- dist(simS)
  #And then use hierarchical clustertering to cluster songs based on the distances
  hc <- hclust(d)
  #In case we want to visualize the dendogran
  #plot(hc)
  
  #Get the similarity between songs from hierarchical clustering and play the songs
  #First find the song to start with
  if (length(startWith) == 0){
    playOrder <- orderSongsC(hc$merge)
  }else{
    playOrder <- orderSongsC(hc$merge, which(mList ==  startWith))}
  
  #Then play songs
  for (i in 1:length(playOrder))  
    play(S[[playOrder[i]]], "/usr/bin/mplayer")
}

#Compile functions
orderSongsC <- cmpfun(orderSongs)
arrangeMusicC <- cmpfun(arrangeMusic)

#An example
arrangeMusicC(inDirectory = getwd())
#arrangeMusicC(inDirectory = "C:/Users/tybug/Music/Google Play Music/The Glitch Mob/Love Death Immortality/se")
