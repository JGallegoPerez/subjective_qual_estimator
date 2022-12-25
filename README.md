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
If you have ever practiced planetary astrophotography, have you noticed when blinking through a set of subframes that, from time to time, a subframe so visually appealing shows up, that you might almost compare it to what could be a final, all-processed image? Although this is all very subjective (that is the motto of the project), it may seem that such *superframes* may appear as rarely as every hundred or several hundreds subframes. Therefore, they have their own space in space in the 
rating procedure. 

### Ratings experimentation
Scores are dynamically saved throughout the rating process in a .CSV file, which can be later explored with Excel or our own IDE tools. Histograms, as well as 
a final summary, tell us about the distributions of the scores, which in turn inform us to decide upon the weights we may want to give to each score. For example,
if we have a scarce set of subs that include one or two superframes, we may not want to assign to the latter weights that are too high. Having an equivalent 
representation in the stack of 10% or more, for example, that subframe would contribute its good appearance, but would also impose its own noise. The final summary
shows the equivalent number of frames that would have been stacked, had there been no weighting (thus, copying of subframes). 

## Procedure

The general procedure consists of the following stages:

(We already start from a subset of a few thousand relatively good subframes, which one may have obtained by pre-quality assessing the subframes 
with the help of applications like PIPP)

**Practice:** from that initial sample, we begin by taking a look at randomly drawn subframes, so that we get a sense of the diversity we are going to encounter 
later throughout the rating process. This is the moment to refine our intutions about what we consider bad or good subframes and why. It can be useful to take 
paper notes in this step, which will help us be more consistent in the scoring later. The program doesn't save any user responses in this stage. 

**Preselection:**  next, we carry out a fast "preselection". Images of each subframe 
are iteratively displayed, which we reject/include for our stack by pressing <,> or <.> on the keyboard, respectively. This can be done at fast pace with the index 
and middle fingers of one hand, but note that we would typically want to have many frames included in our stack. Aim for no less than 800-1000 included frames.

**(Regular) rating:** after having preselected many "acceptable" subframes, we iterate through them again, this time assessing them more finely by assigning a 
score of 1 (worst) to 5 (best: reserved for superframes). This is a lengthy process. It helps to use only the left hand, which each finger other than the thumb 
resting on the keyboard's <1>-<4> number keys. 1-4 will be the most common scores (thus, we will be using mostly those four leftmost fingers). From time to time, we might want to score an image as superframe, for which we will press <5>.

**Superframe rating:** since the superframes will likely have a considerable impact on the final stack, we repeat the previous rating process as before (<1> to <5>), 
but this time with the subframes that we have rated as superframes. 

After having finalized these three stages, we will visualize a summary and a count histogram of the score distributions. These will inform our next decision of 
what weights to assign to each score. At this point, weights identify with the number of copies that will be made for each rated frame. To help us here, we receive 
a prompt that reads "Equivalent original subframes: ". It refers to an improvised, simple algorithm to compute (noise and quality considerations aside) the number 
of original subframes that the final stack equals, supposing we hadn't carried out any weighting. (When we weight some images more than others we actually reduce 
the variability in the final stack, which may be detrimental in reducing noise). This equivalent number is equal or lower (can be *much* lower) than the total 
amount of copies produced for the stack. The algorithm has the shape:

   *equiv_subs =  sum(num_copies / max_copies)*, where num_copies refers to the amount of copies of each image and max_copies is the highest number of copies that 
 has been produced for any single frame. 

The overall procedure may sound complicated, but we are guided by an interactive menu that allows us to move from stage to stage. We can return to the menu anytime by 
pressing <m>, which doesn't reinitialize the program nor eliminates the progress we may have made up to that point. The menu also adds the possibility of *practicing* anytime, just as we did at the beginnng, but within the pipeline stage we are currently in (e.g. if you are in "superframe rating", the practice mode will show you
only random images from the already-rated group and no images that you had already rejected). This can be useful, since after rating many images, or taking a break, 
we may have lost the initial sense of what the subframes we are rating look like. 

###########MENU PICTURE


## .CSV file and experimentation

The program saves a .CSV file, called "*subs_ratings.csv*" that contains the images' names, first/regular ratings, superframe ratings, quality estimations (at this point, identified with the numbers of copies to save for the stack) and stack weights (representing the impact, in percentage, that each weighted image will have over the whole stack), (see Figure below). This file can be opened with .CSV plugins from your IDE of choice, or externally with Excel or other spreadsheet softwares.
  
#############CSV FILE PICTURE 
 
The file is updated every time we rate a new image. It will be overwritten if we start a new session (by pressing <b> to begin another session).
  
We can experiment with different stacking weights at the end of a session, the results of which will show up in the final statistics and will also modify the .CSV
file accordingly. If we run the program and there is data stored in the .CSV file, we can also directly experiment with different stacking weights if we press <q> (from "quality estimation"). Just be careful enough not to press <b>. 
  
  
## Installation and dependencies
  
The initial set of images must be contained in a main directory that must be called "*images*". The program will create other subdirectories in it, containing 
subframes from the various stages in the rating process. The most important of these subdirectories will be "*subframes_copies*", which will contain the images 
to be stacked and can be used directly with other commercial applications, such as AutoStakkert, to stack the images. 
  
The required file format for the images is .tif, but this can be easily modified in the utils.py module, as long as the image file formats are within those 
accepted by OpenCV. 

## Acknowledgments
  
Special thanks to Takazumi Matsumoto for encouragement and inspiration, as well as to Alex Baranski.

################################__init__


