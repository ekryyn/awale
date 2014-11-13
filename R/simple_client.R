send <- function(conn, message_type, message){
  msg = toJSON(list(type=message_type, message=message))
  content = paste0(nchar(msg), "\n\n", msg, sep='')
  
  cat(content)
  writeChar(content, conn, useBytes=TRUE)
}

extract_msg <- function(str){
  message <- ""
  if(nchar(str) > 0){
    pos <- regexec("\n\n", str)[[1]][1] - 1
    if(pos > 0){
      expected_length <- as.numeric(substr(str, 1, pos))
      msg <- substr(str, pos+3, nchar(str))
      if(nchar(msg)>=expected_length){
        message <- substr(msg, 1, expected_length)
        str <- substr(msg, expected_length+1, nchar(msg))
      }
    }
  }
  return(list(message=message, data=str))  
}

plays = c('a', 'b', 'c')
cpt = 1
sock <- socketConnection(host='127.0.0.1', port=1889, server=FALSE)
ins = list(sock)
data <- ""
while(TRUE){
  l = socketSelect(ins, timeout=0)
  if(l[1]){
    d <- readChar(sock, nchars=2048)
    if (d == "") break
    data <- paste(data, d)
  }
  extract <- extract_msg(data)
  msg <- extract[['message']]
  data <- extract[['data']]

  if(nchar(msg) > 0){
    obj <- fromJSON(msg)
    if(obj[['type']] == 'player_id'){
      player_id <- obj[['message']]
    }
    else if(obj[['type']] == 'game_state')
    {
      if(obj[['message']][['to_play']] == player_id)
      {
        # if it's my turn to play :
        send(sock, 'play', plays[cpt])
        cpt <- cpt + 1
      }
    }
  }
}
