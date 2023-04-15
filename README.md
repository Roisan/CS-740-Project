# CS-740-Project

# CS741-Project By 222IS024 & 222IS013

https://github.com/Roisan/CS-740-Project

The implementation of the Raft program is written in the Python language. When executing the program, the user will be prompted to enter the ID of the nodes who will be standing up as candidates. The input ranges from 0 to 4 since a total of 5 nodes have been created. The user is then prompted to enter the votes for the chosen candidates on behalf of the voting nodes. After successful election process, the leader is elected and its logs/entries (which are represented as a string in the program) will be replicated to the follower nodes. An election timeout is programmed to occur after every 5 rounds of log replication after which a new election initiates.

The program will run for a total of 6 rounds which can be altered in the main_loop function. Primary classes inlcude the Node and Raft classes for which the former is used to define the attributes and functions of the simulated node. The various parameters include the node's ID, role, term, vote, log and election timeout counter. Its functions include the req_vote (used to get the vote of the node), app_entries (which is used by the node to append the leader's entries into its log) and dup_log (which is used by the leader to start the log replication process).

The Raft class is responsible for holding the election using the start_election function. The program is designed to select two candidates and the one who gets the majority of the votes will be elected as the leader for the current term. The handle_messages function is used to check of an election timeout has occured in any of the nodes which helps to initiate the election process and to check whether an election has successfully completed. It is also responsible for initiating the leader node to begin the log replication step in case no election timeout occurs.
