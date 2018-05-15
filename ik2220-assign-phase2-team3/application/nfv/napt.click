//define AverageCounter
aveCounter_from_Dmz, aveCounter_to_Dmz, aveCounter_from_Prz, aveCounter_to_Prz :: AverageCounter;

//define counter
arp_Query_eth1, arp_Query_eth2                 :: Counter;
arp_Res_eth1, arp_Res_eth2                     :: Counter;
arp_Query_afterRsp_eth1, arp_Query_afterRsp_eth2                     :: Counter;
icmp_from_Dmz, icmp_from_Prz                   :: Counter;
ip_from_Dmz, ip_from_Prz, ip_count1, ip_count2                      :: Counter;
drop_eth1, drop_eth2, drop_IP1, drop_IP2       :: Counter;


//from Dmz to Prz
from_Dmz :: FromDevice(s10-eth1, METHOD LINUX, SNIFFER false);
to_Prz :: Queue -> aveCounter_to_Prz -> ToDevice(s10-eth2);

//from Prz to Dmz
from_Prz :: FromDevice(s10-eth2, METHOD LINUX, SNIFFER false);
to_Dmz :: Queue -> aveCounter_to_Dmz -> ToDevice(s10-eth1);

arpQuery_toDmz_eth1::ARPQuerier(100.0.0.1, 00:00:00:22:22:01);
arpQuery_toPrz_eth2::ARPQuerier(10.0.0.1, 00:00:00:22:22:02);


//Packet Classifier
eth_Prz_classifier :: Classifier(12/0806 20/0001, 12/0806 20/0002, 12/0800,-);
eth_Dmz_classifier :: Classifier(12/0806 20/0001, 12/0806 20/0002, 12/0800,-);
ip_Prz_classifier, ip_Dmz_classifier :: IPClassifier(icmp,tcp or udp,-)
ip_to_Dmz :: GetIPAddress(16) -> CheckIPHeader -> [0]arpQuery_toDmz_eth1 -> to_Dmz;
ip_to_Prz :: GetIPAddress(16) -> CheckIPHeader -> [0]arpQuery_toPrz_eth2 -> to_Prz;


//Packet rewrite
ip_rw :: IPRewriter(pattern 100.0.0.1 20000-65535 - - 0 1,drop);
ip_rw[0] -> ip_to_Dmz;
ip_rw[1] -> ip_to_Prz;
icmp_rw :: ICMPPingRewriter(pattern 100.0.0.1 20000-65535 - - 0 1,drop);
icmp_rw[0] -> ip_to_Dmz;
icmp_rw[1] -> ip_to_Prz;

//packet from Dmz
from_Dmz ->
	aveCounter_from_Dmz ->
	
	//arp query
	eth_Dmz_classifier[0] ->
		arp_Query_eth1 -> ARPResponder(100.0.0.1 00:00:00:22:22:01) -> arp_Query_afterRsp_eth1 -> to_Dmz;
	
	//arp response
	eth_Dmz_classifier[1] ->
		arp_Res_eth1 -> [1]arpQuery_toDmz_eth1;
	
	//ip packet
	eth_Dmz_classifier[2] ->
		ip_count1 -> Strip(14) -> CheckIPHeader -> ip_Dmz_classifier; 
		
		//icmp
		ip_Dmz_classifier[0] ->
			icmp_from_Dmz -> [1]icmp_rw;
			
		//tcp or udp
		ip_Dmz_classifier[1] ->
			ip_from_Dmz -> [1]ip_rw;
		
		//discard other ip packet
		ip_Dmz_classifier[2] ->
			drop_IP1 -> Discard;
	
	//discard other ethernet packet
	eth_Dmz_classifier[3] ->
		drop_eth1 -> Discard;
		
//packet from Prz
from_Prz ->
	aveCounter_from_Prz ->
	
	//arp query
	eth_Prz_classifier[0] -> 
		arp_Query_eth2 -> ARPResponder(10.0.0.1 10.0.0.0/24 00:00:00:22:22:02) -> arp_Query_afterRsp_eth2 -> to_Prz;
	
	//arp response
	eth_Prz_classifier[1] ->
		arp_Res_eth2 -> [1]arpQuery_toPrz_eth2;
	
	//ip packet
	eth_Prz_classifier[2] ->
		ip_count2 -> Strip(14) -> CheckIPHeader -> ip_Prz_classifier;
		
		//icmp
		ip_Prz_classifier[0] ->
			icmp_from_Prz -> [0]icmp_rw;
			
		//tcp or udp
		ip_Prz_classifier[1] ->
			ip_from_Prz -> [0]ip_rw;
		
		//discard other ip packet
		ip_Prz_classifier[2] ->
			drop_IP2 -> Discard;
	
	//discard other ethernet packet
	eth_Prz_classifier[3] ->
		drop_eth2 -> Discard;
		
// report
DriverManager(wait 1sec, print > ../results/napt.report "
	=================== NAPT Report ===================
	Input Packet Rate (pps): $(add $(aveCounter_from_Dmz.rate) $(aveCounter_from_Prz.rate))
	Output Packet Rate(pps): $(add $(aveCounter_to_Dmz.rate)  $(aveCounter_to_Prz.rate))
	Total # of input packets: $(add $(aveCounter_from_Dmz.count) $(aveCounter_from_Prz.count))
	Total # of output packets: $(add $(aveCounter_to_Dmz.count)  $(aveCounter_to_Prz.count))
	Total # of IP packets: $(add $(ip_count1.count) $(ip_count2.count))
	Total # of ARP requests packets: $(add $(arp_Query_eth1.count) $(arp_Query_eth2.count))
	Total # of ARP respondes packets: $(add $(arp_Res_eth1.count) $(arp_Res_eth2.count))
	Total # of IP requests packets: $(add $(ip_from_Dmz.count) $(ip_from_Prz.count))
	Total # of ICMP packets: $(add $(icmp_from_Dmz.count) $(icmp_from_Prz.count))
	Total # of dropped packets: $(add $(drop_eth1.count) $(drop_eth2.count) $(drop_IP1.count) $(drop_IP2.count))
	ARP Query packet from Prz: $(arp_Query_eth2.count)
	ARP QUERY packet from Dmz: $(arp_Query_eth1.count)
	ARP QUERY packet from Prz after Responder: $(arp_Query_afterRsp_eth2.count)
	ARP QUERY packet from Dmz after Responder: $(arp_Query_afterRsp_eth1.count)
	ICMP packets from Dmz:$(icmp_from_Dmz.count)
	ICMP packets from Prz:$(icmp_from_Prz.count)
	================================================== 
" , loop);








