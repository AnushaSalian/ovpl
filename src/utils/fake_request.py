import requests
import json

adapter_url = "http://10.2.59.57:8000/api/1.0/vm/create"

lab_spec = {
    "lab": {
        "build_requirements": {
            "platform": {
                "arch": "i386",
                "build_steps": {
                    "build": ["make -C ../src"],
                    "configure": [],
                    "post_build": [],
                    "pre_build": [],
                    "status": []
                },
                "installer": [],
                "os": "ubuntu",
                "osVersion": "12",
                "service_pack": ""
            }
        },
        "description": {
            "developer": [
                {
                    "contact": {
                        "alternate_email": "",
                        "email": "jawahar@iiit.ac.in",
                        "mobile_number": "",
                        "office_number": ""
                    },
                    "department": "",
                    "institute": "IIIT Hyderabad",
                    "name": "Jawahar C.V",
                    "organization": "",
                    "role": "Lab Developer",
                    "title": "",
                    "web": ""
                },
                {
                    "contact": {
                        "alternate_email": "",
                        "email": "phani@iiit.ac.in",
                        "mobile_number": "",
                        "office_number": ""
                    },
                    "department": "",
                    "institute": "IIIT Hyderabad",
                    "name": "Phani Phani",
                    "organization": "",
                    "role": "Lab RA",
                    "title": "",
                    "web": ""
                },
                {
                    "contact": {
                        "alternate_email": "",
                        "email": "kumarsrijan@students.iiit.ac.in",
                        "mobile_number": "",
                        "office_number": ""
                    },
                    "department": "",
                    "institute": "IIIT Hyderabad",
                    "name": "Kumar Srijan",
                    "organization": "",
                    "role": "Lab RA",
                    "title": "",
                    "web": ""
                },
                {
                    "contact": {
                        "alternate_email": "",
                        "email": "jayaguru.pandaug08@students.iiit.ac.in",
                        "mobile_number": "",
                        "office_number": ""
                    },
                    "department": "",
                    "institute": "IIIT Hyderabad",
                    "name": "Jay Panda",
                    "organization": "",
                    "role": "Lab RA",
                    "title": "",
                    "web": ""
                },
                {
                    "contact": {
                        "alternate_email": "",
                        "email": "shashank.sharmaug08@students.iiit.ac.in",
                        "mobile_number": "",
                        "office_number": ""
                    },
                    "department": "",
                    "institute": "IIIT Hyderabad",
                    "name": "Shashank Sharma",
                    "organization": "",
                    "role": "Lab RA",
                    "title": "",
                    "web": ""
                }
            ],
            "discipline": [
                "Computer Science & Engineering"
            ],
            "id": "cse02",
            "integration_level": 5,
            "name": "Computer Programming",
            "server-side": True,
            "status": "Released",
            "type": ""
        },
        "runtime_requirements": {
            "platform": {
                "arch": "i386",
                "hosting": "dedicated",
                "installer": [
                    "sudo apt-get update",
                    "sudo apt-get install -y php5 apache2"
                ],
                "lab_actions": {
                    "backup": [],
                    "clean": [],
                    "init": [
                        "cp -r ../build/* /var/www/",
                        "mv /var/www/index.html index.html.default"
                    ],
                    "pause": [],
                    "publish": [],
                    "restore": [],
                    "resume": [],
                    "shutdown": ["service apache2 stop"],
                    "start": ["service apache2 start"],
                    "stats": [],
                    "stop": []
                },
                "memory": {
                    "max_required": "2gb",
                    "min_required": "256mb"
                },
                "os": "ubuntu",
                "osVersion": "12",
                "servicepack": "",
                "storage": {
                    "min_required": "10gb"
                }
            }
        }
    },
    "template": "1.0"
}

payload = json.dumps(lab_spec)
print requests.get(adapter_url)
print requests.post(adapter_url, data=payload)