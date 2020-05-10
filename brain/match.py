sentence_ = "把灯打开"
verb_list = []
adverb_list = []
name_list = []
devices_list = []


def init_device_match():
    read_data('verb.data', verb_list)
    read_data('adverb.data', adverb_list)
    read_data('name.data', name_list)
    read_data('devices.data', devices_list)


def read_data(filename, save_list):
    with open(filename, 'r') as verb_f:
        for line in verb_f:
            line = line.split(':')[0:-1]
            save_list.append(line)
    return save_list


def find_word_in_sentence(word_list, sentence):
    sentence_word_list = []
    sentence = list(sentence)
    print(sentence)
    skip = 0
    for i, the_word in enumerate(sentence):
        if skip > 0:
            skip -= 1
            continue
        for ones in word_list:
            if ones[1] == the_word:
                ones_len = len(ones)
                if ones_len > 2:
                    now_word = the_word
                    now_word_end = ""
                    for j in range(1, int(ones[0])):
                        now_word = now_word + sentence[i + j]
                        for one in ones:
                            if one == now_word:
                                now_word_end = now_word
                        skip = j
                    print(now_word_end)
                    sentence_word_list.append(now_word_end)

                else:
                    print(ones[1])
                    sentence_word_list.append(ones[1])
    return sentence_word_list


def find_device(sentence_word_list):
    the_device = []
    result = {"right":"", "device":"", "option":""}
    count = 0
    for word in sentence_word_list:
        for device in devices_list:
            if device[1] == word:
                print("find a device {}".format(word))
                the_device = device
                result["device"] = word
                count += 1
    for word in sentence_word_list:
        for option in the_device[2:]:
            if option == word:
                print("find option {}".format(word))
                result["option"] = word
                count += 1
    result["right"] = count
    print(result)
    return result


def device_match(sentence):
    print(verb_list)
    print(adverb_list)
    print(name_list)
    words_list = verb_list + name_list + adverb_list
    print(words_list)
    sentence_word_list = find_word_in_sentence(words_list, sentence)
    return find_device(sentence_word_list)


if __name__ == "__main__":
    init_device_match()
    # read_data('verb.data', verb_list)
    # read_data('adverb.data', adverb_list)
    # read_data('name.data', name_list)
    # read_data('devices.data', devices_list)
    # print(verb_list)
    # print(adverb_list)
    # print(name_list)
    # words_list = verb_list + name_list + adverb_list
    # print(words_list)
    # sentence_word_list = find_word_in_sentence(words_list, sentence_)
    # find_device(sentence_word_list)
    device_match(sentence_)
    device_match(sentence_)
