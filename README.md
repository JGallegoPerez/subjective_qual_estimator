# subjective_qual_estimator

This project has been carried out with the main purpose of easing the arduous process of manually selecting astronomical subframes for image stacking, 
which is common practice in amateur (as well as professional) astrophotography.  
Stacking usually involves a small number of subframes in amateur Deep-Sky Object (*DSO*) astrophotography; given that the subframe exposures are very long 
(typically, around 2-10 min), a good (and realistic) night would rarely yield us more than 40-50 usable subframes. In this case, selecting the best 
subframes is easily accomplished with just some visual inspection and by enabling the quality-rating options available in most commercial 
stacking applications. 
However, in contrast to DSO astrophotography, *planetary* astrophotography involves many hundreds or thousands of subframes, taken with exposures as 
short as just a few milliseconds. Here, commercial applications also ease the stacking process by automatically rating and including in the stack 
only the subframes with the highest quality (typically, 1-20% of the subframes in a video file; or around 500-5000 subframes). 

## Automatic quality estimation
Commercial applications, such as PIPP and AutoStakkert, do a great job at sorting the subframes by quality. They rely on methods such as estimating local 
contrast values. For example, according to the PIPP team ([https://sites.google.com/site/astropipp/pipp-manual/quality-options]):
*For the default and original quality algorithms, the quality estimation is based on calculating a summation of local contrast values (sum of squares of 
the difference between adjacent pixels) for a series of subsampled images.  Higher calculated values indicate higher quality images.*

As a whole, the quality algorithms do indeed select good subframes; indeed in a much better way than randomly choosing a percentage. However, if we 
inspect the top-rated images one by one, we may notice that some of them do not appeal to the eye. For example, from a .SER video of Mars with over 50000 
subframes (own acquisition), PIPP's default algorithm rated the first image higher than the second image below (ratings: 98.97% quality,  
versus 98.86%, respectively):

![00023_2022-11-19-1852_7-T-RGB-Mars_f01127_quality_98 87](https://user-images.githubusercontent.com/89183135/209307137-19044abd-2264-45b0-b31a-ab9ed0162d72.jpg)
   *Image rated with 98.97% quality. Supposedly, superior to the image below*


![00024_2022-11-19-1852_7-T-RGB-Mars_f06736_quality_98 86](https://user-images.githubusercontent.com/89183135/209307176-79fc3326-33ed-4b4b-8892-bc57b1b8f5c3.jpg)
   *Image rated with 98.96% quality.*

We might disagree with this quality ordering, and, while not necessarily dismissing the objective overall quality assessments, we may want to also 
consider our own subjective judgments. For instance, I may want to choose for my stacks subframes that have been both automatically rated as good images,
*but also* that satisfy some personal aesthetic requirements: I may want the planet to appear quite round, I may want the image to be sharp enough 
at least in the regions of the disk that are interesting to me, etc. For such a flexible and personal choosing, it seems we have no choice but to hand-
pick our own images. Hundreds or thousands, one by one...

Manually selecting subframes




