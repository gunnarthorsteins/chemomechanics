# voltaiq-acoustics

## Introduction

Batteries are fundamentally electrochemical systems. As such, they're typically viewed through the lens of (electro)chemical engineering. This has worked well for the past half a century or so; Lithium-ion batteries have become omnipresent in the age of advanced electronics. In fact, you're most probably reading this on a device powered by one. And they'll just keep getting more important as we continue to electrify our lives. 

In the utopia that hopefully will be the post-hydrocarbon world we'll have batteries that retain 100% of original capacity for thousands of cycles. Unfortunately, we're not there yet. Batteries do degrade. We've come a long way since [Li-ion batteries](https://en.wikipedia.org/wiki/Lithium-ion_battery) were introduced commercially about thirty years ago, but there's still a plethora of engineering challenges involved in minimizing degradation.

### The Problem: Detecting battery changes as they happen

One of those persistent challenges, one which has eluded battery scientists and engineers for decades, is how to monitor chemo-mechanical properties of batteries _in operando_, i.e. as they cycle. The three-letter acronymic diagnostic tools of chemical engineering (XRD, NMR, SEM, TEM, etc.) are excellent at disentangling phenomena _in situ_ (assembled, not cycling) and _ex situ_ (disassembled), but are lacking _in operando_, at least for full cells. They actually do possess those tools, X-ray would be one, but they all have in common to be prohibitively costly and/or slow.

Electrical engineering tools like voltage and current have instead fulfilled this role. Up until now they've been considered decent enough, especially due to their low cost and ease of deployment, and with the addition of surface temperature sensing they compose the inputs to most modern [BMSs](https://en.wikipedia.org/wiki/Battery_management_system). They are unfortunately imprecise, especially for cell chemistries with flat voltage profiles like [LFP](https://en.wikipedia.org/wiki/Lithium_iron_phosphate_battery).

However, with the ever-increasing demands of modern batteries&mdash;both in terms of safety and optimizing the usage of critical materials ([e.g. increase manufacturing yield](https://www.voltaiq.com/blog/how-to-make-money-manufacturing-batteries-and-why-its-so-hard/))&mdash;we need a tool that packs a real punch. Ideally, such a tool could not just detect degradation events like gassing and cracking, but also spatial heterogeneities. Such a tool could for example give [early indication of thermal runaway](https://www.sciencedirect.com/science/article/pii/S0378775322004335).

### The Solution: Mechanical investigation

Here's the thing. Almost all battery degradation mechanisms manifest in some _mechanical_ symptoms. For example, cracking negatively affects mechanical integrity and gassing reduces density. Luckily for battery researchers there's already a well-established, non-invasive, non-destructive, and relatively cheap methodology to achieve that: **Acoustics**.

Acoustics is the science of emitting and detecting mechanical waves, or soundwaves, and reconstructing the signal to determine mechanical properties of the media through which the waves propagated.

The applications of acoustics underlie such diverse fields as weld inspections, seismology and medical ultrasound imaging, where it's been used for eons. We're all probably most familiar with it in the context of fetal sonograms.

Well, it turns out that it also has applications in battery science and engineering. The principle was first demonstrated in [Hsieh et al](https://pubs.rsc.org/en/content/articlelanding/2015/ee/c5ee00111k), where State-of-Charge (SoC) was shown to be detected. Development has since been continued by various research groups and industry players.

This niche field of battery research has largely been empirically-driven, resulting in incremental process as the datasets involved are small.

Enter Voltaiq.

By leveraging Voltaiq's extensive, harmonized datasets one can test hypotheses without ever having to set a foot in a lab. This accelerates the modeling process: matching model parameters with empirical data grounds the model, if so to speak, before actually having to run acoustics experiments.


## The library

This library was developed as part of Voltaiq's _Voltaiq Community Edition_ (VCE) Fellowship.

It is a small step in the direction of making acoustics for battery characterization more model-driven by generalizing acoustics to any cell, admittedly in a somewhat facile form. The aim was to create a library that could input data from any cell in Voltaiq's database and perform on it a certain piece of analysis.

The analysis in this case is a 1D simulation of acoustic propagation through a battery. 

![Simulation](https://media.giphy.com/media/hPWMNsfZuB2XCUtcSd/giphy.gif)

All one needs is some cell metadata and voltage curves.

### Usage

The functionality can be divided into two steps: (1) preprocessing, and (2) simulation.

1) `example.ipynb` provides a reproducible example on how to run a simulation.

2) `simulation.m` Simply run this (`F5`) to run the simulation. It does not have to be tweaked, unless one wants to change some lower-level parameters. The core is based on the excellent [k-Wave](http://www.k-wave.org/index.php).

Both of these can be run in Voltaiq Analytics Studio. Have fun!