secretKey = "jsanklCNZ257654egbbvnacm54andjkc7snaxca8zcwdcwscms1"
verificationKey ="QVQKLa8zVQKLwdVQKLwsVQKLms1djkVQKL7snQVQKLjsank4egbbvnaVQKLm54an25765a8zVQKLwdVQKLwsVQKLms1naVQKLm54andjkVQKL7snlCNZ257654egbbvjsanklCNZ"
emailKey = "13761foff534156137976656765460357387663456624829738423798937967657668765676546035645354665064532302765575"
admin_secret = "vyuewgqfhscjkwlsbfvhdwkjakxmsnxjksdvfdjskaxm,"


def specialEncoder(email):
    parts = email.split("@")
    encoding = secretKey[:9:]+parts[0][::-1]+emailKey[:18:]+parts[1][::-1]
    return encoding


def specialDecoder(link):
    if link[:9:] == secretKey[:9:]:
        link = link[9::]
        link = link[::-1]
        domain, username = link.split(emailKey[:18:][::-1])
        email = "{}@{}".format(username, domain)
        return email
