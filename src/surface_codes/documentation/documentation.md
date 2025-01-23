# Basics of Error correction

The general structure of an error correcting code is as follows:
![Error correction circuits in general - source https://opencourse.inf.ed.ac.uk/sites/default/files/https/opencourse.inf.ed.ac.uk/iqc/2024/iqclecture29_0.pdf](assets/QECC_circuit.png)

- Encoding - Encode our state using ancilla qubits
- Error - Some errorrs occur
- Stabilizer measurements - Measure the ancilla qubits to detect the errors. This is done by measuring the stabilizers of the code.
- Recovery - Correct the errors by applying the appropriate correction operations.

## Stabilizers
![arthur UCL blog](assets/image-12.png)

Soo, Stabilizers are an Abelian group meaning they need to comute, thus we want to have even # of X and Z operators intersect (see below more comprehensive explanation). 


Measure all the stabilizers, resulting in what is called the syndrome.

While stabilizers of the same Pauli type necessarily commute, it is not obvious that all the $Z$ stabilizers commute with all the $X$ stabilizers. For this to be the case, each $X$ stabilizer should intersect on an even number of qubits with all the $Z$ stabilizers 

### Steane code - color code

![alt text](assets_2/image.png)

![alt text](assets_2/image-2.png)

!Note. Furthermore, it only requires the measurement of weight-4 stabilizers, as opposed to Shor’s code which requires measuring weight-6 stabilizers. Since errors can happen during the measurement of stabilizers, a good rule of thumb to get well-performing quantum codes is to always try to minimize the weight of its stabilizer generators.

![alt text](assets_2/image-1.png)

![alt text](assets_2/image-3.png)

![- https://en.wikipedia.org/wiki/Centralizer_and_normalizer](assets_2/image-4.png)


![Logical operators - cx gate of steane code - https://abdullahkhalid.com/blog/2022/Nov/01/logical-operations-for-the-steane-code/](image.png)

![Steane correct broken qubits - https://stem.mitre.org/quantum/error-correction-codes/steane-ecc.html](image-1.png)

# Surface codes


## Why would we want to use surface codes ?

So far we have seen many kinds of codes, but most of them were handcrafted, and so a lot of atention needs to be put into making them. Thus:
![Goal of scaling CSS - source https://opencourse.inf.ed.ac.uk/sites/default/files/https/opencourse.inf.ed.ac.uk/iqc/2024/iqclecture29_0.pdf](assets/image.png)

Some major advantages that this kind of codes also have are:
![Advantages of surface codes - source https://opencourse.inf.ed.ac.uk/sites/default/files/https/opencourse.inf.ed.ac.uk/iqc/2024/iqclecture29_0.pdf](assets/image-2.png)

In general when dealing with surface codes we have to keep in mind the following threshold: (basically, untill when it is still worth it to add even more physical qubits, to get a better error rate)
![alt text](assets/image-9.png)

Fun fact:

![alt text](assets/image-10.png)


## 4-cycle - basic structure behind surface codes
For starters to get used to surface codes we implement the most basic form of one such code, the 4-cycle surface code. This code is defined on a 2D lattice of qubits, where each qubit is connected to its nearest neighbors.  

![Tanner graph of basic 4-cycle surface code - source https://opencourse.inf.ed.ac.uk/sites/default/files/https/opencourse.inf.ed.ac.uk/iqc/2024/iqclecture29_0.pdf](assets/4-cycle.png)

A better way to understand the same graph:
![a better representation of the 4-cycle code - source https://arxiv.org/pdf/1907.11157](assets/image-1.png)

There are two kinds of qubits that we use in the 4-cycle code:
- Data qubits - These are the qubits that store the information that we want to protect.
- Ancilla qubits - These are the qubits that we use to detect the errors. We measure the stabilizers of the code using these qubits.

This can be seen even better in the below ilustration:
![alt text](assets/image-3.png)

![alt text](assets/image-4.png)

## More general surface codes

Error detection:

![alt text](assets/image-5.png)

![alt text](assets/image-6.png)


![alt text](assets/image-7.png)

Since they anti commute it means that they behave just as for the regular qubit.

!Note. We always want to have an extra degree of freedom, that's why we always have more data qubits than ancilla qubits.

![alt text](assets/image-8.png)



### What is next ?

![alt text](assets/image-11.png)


# References

- Explanation about stabilizers and surface codes basics, with amazing visualizations - https://arthurpesah.me/blog/
- Introductory course with nice visualizations - https://opencourse.inf.ed.ac.uk/sites/default/files/https/opencourse.inf.ed.ac.uk/iqc/2024/iqclecture29_0.pdf
- general introduction into quantum error correcting codes -https://arxiv.org/pdf/1907.11157
- Surface codes *for the mortals* **the best resource** - https://journals.aps.org/pra/abstract/10.1103/PhysRevA.86.032324
- https://en.wikipedia.org/wiki/Centralizer_and_normalizer
- more about logical operators of Steane code - https://abdullahkhalid.com/blog/2022/Nov/01/logical-operations-for-the-steane-code/
- steane qubits problems - https://stem.mitre.org/quantum/error-correction-codes/steane-ecc.html