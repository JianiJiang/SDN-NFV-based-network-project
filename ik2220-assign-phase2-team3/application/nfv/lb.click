//define AverageCounter
aveCounter_input_eth1, aveCounter_output_eth1, aveCounter_input_eth2, aveCounter_output_eth2 :: AverageCounter;

//define counter
arp_Query_eth1, arp_Query_eth2				 :: Counter;
arp_Res_eth1, arp_Res_eth2				:: Counter;
ip_output_eth1, ip_output_eth2, icmp_count1, icmp_count2,ip_count1                  :: Counter;
drop_input_eth1, drop_input_eth2, drop_input_IP1       :: Counter;


// from client to server
from_client_eth1 :: FromDevice($Name-eth1, METHOD LINUX, SNIFFER false);
to_server_eth2 :: Queue -> aveCounter_output_eth2 -> ToDevice($Name-eth2);

//from server to client
from_server_eth2 :: FromDevice($Name-eth2, METHOD LINUX, SNIFFER false);
to_client_eth1 :: Queue -> aveCounter_output_eth1 -> ToDevice($Name-eth1);

//packet classifier
eth_A1_classifier ::Classifier(12/0806 20/0001, 12/0806 20/0002, 12/0800,-);
eth_A2_classifier ::Classifier(12/0806 20/0001, 12/0806 20/0002, 12/0800,-);
ip_classifier :: IPClassifier(icmp, dst $proto port $port,-);

//ARP packet
arpQuery_toServer_eth2 :: ARPQuerier($VIP, 00:00:00:22:22:$MAC1);
arpQuery_toClient_eth1 :: ARPQuerier($VIP, 00:00:00:22:22:$MAC0);

ip_to_client :: GetIPAddress(16) -> CheckIPHeader -> [0]arpQuery_toClient_eth1  -> to_client_eth1;
ip_to_server :: GetIPAddress(16) -> CheckIPHeader -> [0]arpQuery_toServer_eth2 -> to_server_eth2;
//Packet rewrite
server_round :: RoundRobinIPMapper(
	$VIP - $DIP0 - 0 1, 
	$VIP - $DIP1 - 0 1, 
	$VIP - $DIP2 - 0 1);
ip_rw :: IPRewriter(server_round, pattern $VIP 20000-65535 - - 1 0)
ip_rw[0] -> ip_to_server;
ip_rw[1] -> ip_to_client;

//pakcet from server
from_server_eth2 ->
	aveCounter_input_eth2 ->
	
	//ARP query
	eth_A2_classifier[0] ->
		arp_Query_eth2 -> ARPResponder($VIP 00:00:00:22:22:$MAC0) -> to_server_eth2;
	
	//ARP response
	eth_A2_classifier[1] ->
		arp_Res_eth2 -> [1]arpQuery_toServer_eth2;
	
	//IP packet
	eth_A2_classifier[2] -> 
		ip_output_eth1 ->Strip(14) -> CheckIPHeader -> [1]ip_rw;	
	
	//discard other ethernet packet
	eth_A2_classifier[3] ->
		drop_input_eth2 -> Discard;

//packet from client
from_client_eth1 ->
	aveCounter_input_eth1 ->
	
	//ARP query
	eth_A1_classifier[0] ->
		arp_Query_eth1 -> ARPResponder($VIP 00:00:00:22:22:$MAC1) -> to_client_eth1;
	
	//ARP response
	eth_A1_classifier[1] ->
		arp_Res_eth1 -> [1]arpQuery_toClient_eth1;
	
	//IP packet
	eth_A1_classifier[2] -> 
		ip_output_eth2 -> Strip(14) -> CheckIPHeader ->
		
		//icmp
		ip_classifier[0] ->
			icmp_count1 -> ICMPPingResponder -> icmp_count2-> ip_to_client;

		//tcp or udp
		ip_classifier[1] ->
			ip_count1 -> [0]ip_rw;
		//other
		ip_classifier[2] ->
			drop_input_IP1 -> Discard;
	
	//discard other ethernet packet
	eth_A1_classifier[3] ->
		drop_input_eth1 -> Discard;
// report
DriverManager(wait 1sec, print > ../results/$(Report).report "
	=================== $Report Report ===================
	Input Packet Rate (pps): $(add $(aveCounter_input_eth1.rate) $(aveCounter_input_eth2.rate))
	Output Packet Rate(pps): $(add $(aveCounter_output_eth1.rate)  $(aveCounter_output_eth2.rate))
	Total # of input packets: $(add $(aveCounter_input_eth1.count) $(aveCounter_input_eth2.count))
	Total # of output packets: $(add $(aveCounter_output_eth1.count)  $(aveCounter_output_eth2.count))
	
	Total # of ARP requests packets: $(add $(arp_Query_eth1.count) $(arp_Query_eth2.count))
	Total # of ARP respondes packets: $(add $(arp_Res_eth1.count) $(arp_Res_eth2.count))

	Total # of service packets: $(add $(ip_count1.count) $(ip_output_eth1.count))
	Total # of ICMP packets: $(icmp_count1.count)
	Total # of dropped packets: $(add $(drop_input_eth1.count) $(drop_input_eth2.count) $(drop_input_IP1.count))
	ARP Q From Server: $(arp_Query_eth2.count)
	ARP Q From Client: $(arp_Query_eth1.count)
	tcp or udp packet from client: $(ip_count1.count)
	ICMP packet from client after responder: $(icmp_count2.count)
	================================================== 
" , loop);
