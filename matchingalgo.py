#function to check if the user is a learner of sharer; userData is a dictionary
def learnerOrSharer(userData):
    if len(userData['interested_comms_id'])/len(userData['my_comms_id']) > 1:
        return "learner"
    else:
        return "sharer"

#function to return 0 or best match user id; userData is a dictionary, dbData is array of dictionary
def compatibilityCheck(userData, dbData):
    user_interested_comms = userData['interested_comms_id'] #user interested comms
    user_identified_comms = userData['my_comms_id'] #user identified comms
    best_score = 0 #var to keep track of the best score
    best_match_id = 0 #var to keep track of the user with the best score
    desired_match_type = 'sharer' if userData['status'] == 'learner' else 'learner'
    for person in dbData:
        if person['status'] != desired_match_type or person['match_status'] != 'waiting':
            continue
        identified_score  = 0
        for comm in user_identified_comms:
            if comm in person['interested_comms_id']:
                identified_score += 1
        interested_score = 0
        for comm in user_interested_comms:
            if comm in person['my_comms_id']:
                interested_score += 1
        if identified_score == 0 or interested_score == 0: #either the user do not have what the match wants or vice versa
            continue
        elif (identified_score + interested_score) > best_score: #best match thus far, update details
            best_score = identified_score + interested_score
            best_match_id = person['uuid']
    return best_match_id