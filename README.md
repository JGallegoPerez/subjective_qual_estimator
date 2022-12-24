# subjective_qual_estimator


This project has been carried out with the main purpose of easing the arduous process of manually selecting astronomical subframes for image stacking, 
which is common practice in amateur (as well as professional) astrophotography.  
Stacking usually involves a small number of subframes in amateur Deep-Sky Object (*DSO*) astrophotography; given that the subframe exposures are very long 
(typically, around 2-10 min), a good (and realistic) night would rarely yield us more than 40-50 usable subframes. In this case, selecting the best 
subframes is easily accomplished with just some visual inspection and by enabling the quality-rating options available in most commercial 
stacking applications. 
However, in contrast to DSO astrophotography, *planetary* astrophotography involves many hundreds or thousands of subframes, taken with exposures as 
short as just a few milliseconds. Here too, commercial applications can ease the stacking process by automatically rating and including in the stack 
only the subframes with the highest quality (typically, 1-20% of the subframes in a video file; or around 500-5000 subframes). 

## Automatic quality estimation
Commercial applications, such as PIPP and AutoStakkert, do a great job at sorting the subframes by quality. They rely on methods such as estimating local 
contrast values. For example, according to the PIPP team (https://sites.google.com/site/astropipp/pipp-manual/quality-options):
*For the default and original quality algorithms, the quality estimation is based on calculating a summation of local contrast values (sum of squares of 
the difference between adjacent pixels) for a series of subsampled images.  Higher calculated values indicate higher quality images.*

As a whole, the quality algorithms tend to select good subframes; indeed in a much better way than randomly choosing a percentage. However, if we 
inspect the top-rated images one by one, we may notice that some of them might not appeal to the eye. For example, from one .SER video of Mars with over 50000 
subframes (own acquisition), PIPP's default algorithm rated the first image below higher than the subsequent image, even though the latter 
might look better to most people (ratings: 98.97% quality, versus 98.86%, respectively):

![00023_2022-11-19-1852_7-T-RGB-Mars_f01127_quality_98 87](https://user-images.githubusercontent.com/89183135/209307137-19044abd-2264-45b0-b31a-ab9ed0162d72.jpg)

   *Image rated with 98.97% quality. Supposedly, superior to the image below.*


![00024_2022-11-19-1852_7-T-RGB-Mars_f06736_quality_98 86](https://user-images.githubusercontent.com/89183135/209307176-79fc3326-33ed-4b4b-8892-bc57b1b8f5c3.jpg)

   *Image rated with 98.96% quality.*

## Manually selecting subframes

We might disagree with this quality ordering, and, while not necessarily dismissing objective overall quality assessments, we may want to also 
consider our own subjective judgments. For instance, I may want to choose for my stack subframes that have been both automatically rated as good images,
but that *also* satisfy some personal aesthetic requirements: I may want the planet to appear quite round, I may want the image to be sharp enough 
at least in the regions of the disk that I'm mostly interested in, etc. For such a flexible and personal choosing, it seems we have no choice but to hand-
pick our own images. Hundreds or thousands, one by one...
This is where the present project comes into play.

## Purpose of this project 

The program allows us to rate our astronomical images one by one, subjectively, according to our own aesthetic preferences. The ratings serve a double purpose: 
1) Weighted stacking: the ratings correspond to weights according to which the program will create more or less copies of the selected subframes (for stacking).
2) Later experimentation: the ratings, as well as other values, are saved in a .CSV file that can be later reused to experiment, for example, with different 
stacking weights, or as labels for Machine Learning applications.

### Weighted stacking

Applications like PIPP offer us the possibility to increase the number of copies of the best subframes that are to be stacked. This is a way of increasing the impact
of the best subframes in the final stacked image. This project addresses weighted copying too, but with more flexibility. We are able to assign different weights to the different rating scores. Furthermore, we introduce the concept of *superframes*, which are treated separatedly from the rest of frames. 
#### Superframes
If you have practiced planetary astrophotography, have you noticed when blinking through a set of subframes that, from time to time, a subframe so visually appealing 
shows up, that we might almost compare it to what could be a final, all-processed image. Although this is all very subjective (that is the motto of the project), 
it may seem that such *superframes* may appear as rarely as every hundred or several hundreds subframes. Therefore, they have their own space in space in the 
rating procedure. 

### Ratings experimentation
Scores are dynamically saved throughout the rating process in a .CSV file, which can be later explored with Excel or our own IDE tools. Histograms, as well as 
a final summary, tell us about the distributions of the scores, which in turn inform us to decide upon the weights we may want to give to each score. For example,
if we have a scarce set of subs that include one or two superframes, we may not want to assign to the latter weights that are too high. Having an equivalent 
representation in the stack of 10% or more, for example, that subframe would contribute its good appearance, but would also impose its own noise. The final summary
shows the equivalent number of frames that would have been stacked, had there been no weighting (thus, copying of subframes). 



## Procedure in a nutshell 







Special thanks to Takazumi Matsumoto for .. and to Alex Baranski for...




