#!/bin/awk -f

{
NumberOfWords++
oneWordMap[$1]++
biWordMap[$0]++
}
END{
 print iword
  for(j in biWordMap){
        split(j,a," ")
      if(a[1]==iword || a[2]==iword){
             mim=biWordMap[j]/(oneWordMap[a[1]] * oneWordMap[a[2]])
             emim=biWordMap[j] * log(NumberOfWords * mim)
             chisq=((biWordMap[j] - (1/NumberOfWords) * oneWordMap[a[1]] * oneWordMap[a[2]]) * (biWordMap[j] - (1/NumberOfWords) * oneWordMap[a[1]] * oneWordMap[a[2]])/(oneWordMap[a[1]] * oneWordMap[a[2]]))
             dc=biWordMap[j]/(oneWordMap[a[1]] + oneWordMap[a[2]])
	     if (a[1]==iword)
	       temp = a[2]
	     else
	       temp = a[1]
             printf("%s %f MIM \n",temp,mim)
             printf("%s %f EMIM \n",temp,emim)
             printf("%s %f CHISQ \n",temp,chisq)
             printf("%s %f DICE \n",temp,dc)

      }

  } 
}

