# About DAO-Analyzer

DAO-Analyzer is a web dashboard that shows the state and evolution of
DAOs. In particular, you can see, among other things, the number of DAO
members and how active they are, the evolution of proposals the DAO
votes on, and the state of cryptoassets and cryptotokens that the DAO
manages.

## What is a DAO?

DAO stands for Decentralized Autonomous Organization. A DAO is an
organization that mediates through blockchain and that enables new ways
of collectively running a project, typically by voting proposals and
allocating cryptofunds.

## Which DAOs does DAO-Analyzer monitor?

DAO-analyzer monitors, so far, the DAOs from the following platforms:
**DAOhaus**, **Aragon** and **Daostack**. These platforms facilitate the
deployment of a DAO in a blockchain and the interaction of the DAO
members with the DAO.

While each DAO platform provides different ruling mechanisms for DAOs,
they all essentially provide mechanisms for voting and for the
allocation of cryptofunds.

## Where are the DAOs running?

The DAOs that we monitor are running on public blockchains. Mainly, in
the Ethereum *mainnet*, that is, the primary public Ethereum blockchain
network. However, in recent times, DAO platforms make it possible to
deploy and operate a DAO in other chains, such as *xDai* or *Polygon*,
that are designed to address Ethereum *mainnet* issues like slow
transactions, high fees and throughput problems. DAO-Analyzer also
monitors the DAOs in such networks.

## How does DAO-Analyzer get the data?

DAO-Analyzer retrieves the data from the different blockchains using
[The Graph](https://thegraph.com), an indexing protocol for
querying decentralized networks such as Ethereum, xDai, Polygon, etc.
Using this protocol, **we get the public data stored on the blockchain**
about each DAO.

In the blockchain, there is a record of every action made by the DAO
software (remember that a blockchain can be viewed as a decentralized
database). Thus, we use the *The Graph* protocol to query the blockchain
and retrieve information about the DAO: membership, assets, voting, etc.

## Who develops DAO-Analyzer?

We are researchers of the [GRASIA research
group](http://grasia.fdi.ucm.es/) of [Universidad Complutense de
Madrid](https://www.ucm.es/).

In particular, DAO-Analyzer is created under the umbrella of two
research projects: Chain Community, funded by the Spanish Ministry of
Science and Innovation (RTI2018‐096820‐A‐I00) and led by Javier Arroyo
and Samer Hassan; and [P2P Models](https://p2pmodels.eu/), funded
by the European Research Council (ERC-2017-STG 625 grant no.: 75920),
led by Samer Hassan.

The programmers of this project were formerly [Youssef El Faqir El
Rhazoui](https://github.com/FRYoussef) and currently [David Davó
Laviña](https://github.com/daviddavo), [Elena Martínez Vicente](https://www.linkedin.com/in/elenamartinezvicente/) is in
charge of the UI/UX and [Javier Arroyo](https://scholar.google.es/citations?hl=en&user=XnLmmE8AAAAJ) leads the development of the
product.

DAO-Analyzer is free open source software and we develop it in the open.
You can have a look at the code on
[Github](https://github.com/Grasia/dao-analyzer).

Also, you can follow us on [Twitter](https://twitter.com/p2pmod).

## How can I know more?

If you are interested, you can read more information about DAO-Analyzer
and the research papers based on it.

-   A [post for humans](https://www.google.com/url?q=https://p2pmodels.eu/dao-analyzer-a-tool-to-monitor-dao-activity/&sa=D&source=docs&ust=1651506831958697&usg=AOvVaw3vYMxYsphZ98n1VxgHzY2u) in the P2P Models website.

-   Our research [paper in OpenSym 2020](https://opensym.org/wp-content/uploads/2020/08/os20-paper-a11-el-faqir.pdf), where we presented the tool and showed its use with a case study.

-   Out research [paper in HICSS 2021](https://scholarspace.manoa.hawaii.edu/bitstream/10125/71296/0543.pdf), where we use the tool to have a look at the voting system of the DAOstack platform.

-   Our “late breaking work” [paper presented at CHI 2021](https://dl.acm.org/doi/pdf/10.1145/3411763.3451755?casa_token=cU40LWnMO0EAAAAA:608tLS07Ya0KuhrBXihSSCRqMV72jDOu0XfP3jXnH64z4c2glcY43w69feOikee4t2oxoQ4doxAFjg), where we investigated the effect of the increase in the Ethereum transaction costs and the activity in DAOs.

-   Our [article in the Journal of Internet Services and Applications](https://jisajournal.springeropen.com/articles/10.1186/s13174-021-00139-6), where we compare the evolution of three DAO platforms.

-   Our [extended-abstract](https://doi.org/10.1145/3500868.3559707) from the demo performed at CSCW 2022, where we present the current state of the application and its architecture.

Stay tuned for more!
