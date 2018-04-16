def read_html_pages_in_dir(pages_dir):
    dict_mails={}
    ##Un dictionnaire de mails contenant: +Date
    ##                                    +Auteur(nom/mail)
    ##                                    +Sujet
    ##


    #rootdir="./DHFR_sample/"
    for subdir, dirs, files in os.walk(pages_dir):
#ON VA LIRE TOUS LES FICHIERS DU REP ROOTDIR
        for file in files:
    #V1     if file.endswith('.html') == True  and file != ("index.html") and not re.match("mail\d+.html",file) :
           if re.match("msg\d+.html",file) :

            # les index.html sont des recap, on pourrait les compter pour s'assurer du nombre de messages

                print "\n",os.path.join(subdir, file), "\n"
                champs_auteur={}
                filename=os.path.join(subdir, file)
                soup=BeautifulSoup(open(filename, 'r').read(),'lxml')#, 'html.parser')
#RECUPERER LE SUJET DU MESSAGE

                
                for zone_cible in soup.findAll('ul'):
                    sujet_messg = zone_cible.find(string=re.compile(": \[DH\]"))
                    zone_de_metadonnees_auteur = None
                    i=0
                    for ZC in zone_cible.findAll('strong'):
#TESTER QUE LA ZONE EST BIEN FORMEE
                        i+=1
                        zone_de_metadonnees = zone_cible.strong.parent
                        print zone_de_metadonnees_auteur,"\n\n",i
                        if sujet_messg is not None:
                         if zone_de_metadonnees_auteur is not None:
                          print "ZMA \n",zone_de_metadonnees_auteur
                          if '<li><strong>From</strong>:' in str(zone_de_metadonnees_auteur):
                          #if r'<li><strong>To</strong>: ' in zone_de_metadonnees_auteur:
                            print zone_de_metadonnees_auteur

                            zone_de_metadonnees_destinataires = zone_cible.strong.parent.parent
                            print "NEXT ELEM", zone_de_metadonnees_destinataires

	##EXEMPLE:
	##_______________
	####<li><strong>From</strong>: Eric Guichard &lt;
	## <script type="text/javascript">
	## <!--
	## document.write("Eric.Guichard" + "@" + "enssib.fr")
	## // -->
	## </script>&gt;</li>
	##NOM Eric Guichard
	##MAIL  Eric.Guichard@enssib.fr
	##: [DH] école d'été Méthodes digital es pour SHS - Lyon - 16-20 septembre
	##Eric Guichard
	##
	##
	## Eric.Guichard@enssib.fr
	####./DHFRsample/2013-07/msg00018.html

#RECUPERER L AUTEUR DU MESSAGE
	#PARSAGE DE L HTML AUTEUR
                            zone_de_metadonnees_auteur_nettoye  = re.sub(r'<li><strong>From</strong>: ', '',str(zone_de_metadonnees_auteur))
                            #re.compile(re.escape("\" &lt; <script type=\"text/javascript\"> <!\-\-  document\.write(\""))
                            zone_de_metadonnees_auteur_nettoye = re.sub(r' &lt;.*', '',str(zone_de_metadonnees_auteur_nettoye))
                            zone_de_metadonnees_auteur_nettoye= re.sub(r"<script type=\"text/javascript\">",'',str(zone_de_metadonnees_auteur_nettoye))
                            zone_de_metadonnees_auteur_nettoye= re.sub(r"<!--",'',str(zone_de_metadonnees_auteur_nettoye))
                            zone_de_metadonnees_auteur_nettoye= re.sub("document.write\(\"",'',zone_de_metadonnees_auteur_nettoye)
                            zone_de_metadonnees_auteur_nettoye= zone_de_metadonnees_auteur_nettoye.replace("\" + \"@\" + \"",'@')
                            zone_de_metadonnees_auteur_nettoye= re.sub(r"\"\)\n // \-\->\n </script>&gt;</li>","",zone_de_metadonnees_auteur_nettoye)
                            zone_de_metadonnees_auteur_nettoye= re.sub(r"\"\)\n // \-\->\n </script></li>","",zone_de_metadonnees_auteur_nettoye)



                            nom= zone_de_metadonnees_auteur_nettoye.split("\n")[0]
                            try:
                                mail= zone_de_metadonnees_auteur_nettoye.split("\n")[3]
                            except:
                                print "###",zone_de_metadonnees_auteur_nettoye.split("\n")
                                print "\n",os.path.join(subdir, file), "\n"
                                print zone_de_metadonnees_auteur
                                next( ZC)

                            print "NOM",nom
                            print "MAIL",mail
                            champs_auteur["nom_auteur"]=  nom
                            champs_auteur["mail_auteur"]=  mail
                            champs_auteur["ref_physique_de_l_article"]=  os.path.join(subdir, file)
                            champs_auteur["sujet_du_message"] = sujet_messg
                            print sujet_messg
                            #print zone_de_metadonnees_auteur1
                            print zone_de_metadonnees_auteur_nettoye

                            dict_auteur_mail[champs_auteur["ref_physique_de_l_article"]]=champs_auteur
                            #AFFICHAGE DBG
                            print "\n",os.path.join(subdir, file), "\n"
                            print "_______________\n"
                            break


#RECUPERER LES DESTINAIRES DU MESSAGE
                    #zone_de_metadonnees_destinataires = zone_cible.strong.parent.next_element
                    #print "NEXT ELEM", zone_de_metadonnees_destinataires

#RECUPERER LES CC DU MESSAGE

#RECUPERER LES DATES ET HEURES DU MESSAGE


#AFFICHAGE NOM DE FICHIER TRAITE
#                print "\n",os.path.join(subdir, file), "\n"
#                print "_______________\n"



    return dict_auteur_mail
