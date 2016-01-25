Service Oriented Computing Lab 7
====
Hands on ESB
Name: Weiyi Wang
weiyi.wang@sv.cmu.edu

-------------------------

Description
------
This project is based on [Mule ESB](www.mulesoft.com). It includes some simple usage of the Mule ESB. Please refer to the documents below for more information.

Files
------
There are one folder and some files included in the tarball. The folder Helloworld includes a Mule project which can be imported to Mule Anypoint Studio. The files are this readme file and a pdf of the open question according to the requirements on the assignment.

The three screenshots are
1. screenshot_helloworld: The screenshot for helloworld to Mule
2. screenshot_content_based_dispatch: The screenshot for content based dispatching in Mule
3. screenshot_rr: The roundrobin implementation of (2)

HOW TO RUN
------
To run the project, you need to download the Anypoint Studio on the [Mule Website](www.mulesoft.com). It's a mod of Eclipse and you can import the project to the studio.

After the project is imported in the Anypoint Studio:
1. Right click on the helloworld project and select Run as/Mule Application. The app will be started in no time.
2. In your web browser go to localhost:10086. You will see a greeting in it.
3. On localhost:10087, there is a content based routing example. You can visit endpoints like http://localhost:10087/?language=French or French, Chinese, English to recive greetings of different languages. You can also just visit http://localhost:10087 to have a round robin message dispatch.

Question Two
------
The question two of the lab can be found in the lab_report_weiyiwang.pdf . Please check!