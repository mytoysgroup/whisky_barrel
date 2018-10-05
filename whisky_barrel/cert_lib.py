from __future__ import print_function
import os,sys,shutil,base64,stat
from subprocess import check_output


#deprecated as it only support up to 1024 bits
def create_ssh_host_keys_deprecated(target_dir,bits=4096):
    from Crypto.PublicKey import RSA, DSA
    def create_files(key,infix):
        file = target_dir + '/ssh_host_%s_key'%infix
        file_pub =  rsa_file + '.pub'
        with open(file,'w') as handle:
            os.chmod(file,0600)
            handle.write(key.exportKey('PEM'))

        with open(file_pub,'w') as handle:
            handle.write(key.publickey().exportKey('OpenSSH'))


    rsa_key = RSA.generate(bits)
    dsa_key = DSA.generate(bits)

    create_files(rsa_key,'rsa')
    create_files(dsa_key,'dsa')

def establish_ssh_server_keys(profile,target_dir):
    'Outputs json, to be called from Terraform'

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    print('{')
    for infix in ('rsa','dsa','ecdsa','ed25519'):
        f = "%s/ssh_host_%s_key" % (target_dir,infix)
        if os.path.exists(f + '.kms') and os.path.exists(f + '.pub'):
            print("INFO: Using existing %s.kms and %s.pub"%(f,f),file=sys.stderr)
        else:
            print("INFO: Creating %s"%f,file=sys.stderr)
            for suffix in ('','.kms','.pub'):
                if os.path.exists(f + suffix):
                    os.unlink(f + suffix)
            os.system("ssh-keygen -f %s -N '' -t %s 1>&2"%(f,infix))
            kms_encrypt_file(profile,f)
        print('  "%s": "%s.kms",'%(infix,f))
        print('  "%s_pub": "%s.pub",'%(infix,f))
    print('  "__":""') #instead of removing the last comma
    print('}')

def establish_ssh_login_key(name,profile,target_dir,bits=4096):
    'Outputs json, to be called from Terraform'

    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    dot_ssh_file=os.path.expanduser('~/.ssh/%s.%s.id_rsa'%(name,profile))
    f = "%s/id_rsa" % target_dir
    print('{')
    if os.path.exists(f+'.kms') and os.path.exists(f+'.pub'):
        print("INFO: Using existing %s.kms and %s.pub"%(f,f),file=sys.stderr)
        if not os.path.exists(dot_ssh_file):
            shutil.copyfile(f+'.kms',dot_ssh_file+'.kms')
            shutil.copyfile(f+'.pub',dot_ssh_file+'.pub')
            print("INFO: Creating %s and %s.pub"%(dot_ssh_file,dot_ssh_file),file=sys.stderr)
            kms_decrypt_file(profile,dot_ssh_file+'.kms')
            os.chmod(dot_ssh_file,stat.S_IREAD|stat.S_IWRITE)
        else:
            print("INFO: Using existing %s and %s.pub"%(dot_ssh_file,dot_ssh_file),file=sys.stderr)
    else:
        print("INFO: Creating %s"%f,file=sys.stderr)
        for suffix in ('','.kms','.pub'):
            if os.path.exists(f + suffix):
                os.unlink(f + suffix)
        os.system("ssh-keygen -f %s -N '' -t rsa -b %i 1>&2"%(f,bits))
        if not os.path.exists(dot_ssh_file):
            print("INFO: Creating %s and %s.pub"%(dot_ssh_file,dot_ssh_file),file=sys.stderr)
            shutil.copyfile(f,dot_ssh_file)
            shutil.copyfile(f+'.pub',dot_ssh_file+'.pub')
            os.chmod(dot_ssh_file,stat.S_IREAD|stat.S_IWRITE)
        else:
            print("INFO: Using existing %s and %s.pub"%(dot_ssh_file,dot_ssh_file),file=sys.stderr)
        kms_encrypt_file(profile,f)

    print('  "rsa": "%s.kms",'%f)
    print('  "rsa_pub": "%s.pub",'%f)
    print('  "__":""') #instead of removing the last comma
    print('}')

def kms_decrypt_file(profile,kms_enc_file):
    #removes original if successful
    if kms_enc_file.endswith('.kms'):
        kms_dec_file=kms_enc_file[:-4]
    else:
        raise Exception('File does not end in .kms: %s' % kms_enc_file)
    
    with open(kms_enc_file,'r') as h:
        b64enc_input = h.read()
    b64dec_input = base64.b64decode(b64enc_input)
    b64dec_input_file = kms_dec_file + '.d64'
    with open(b64dec_input_file,'w') as h:
        h.write(b64dec_input)

    b64enc_output = check_output(["aws","--profile", profile, "kms","decrypt","--ciphertext-blob","fileb://"+b64dec_input_file,"--query","Plaintext","--output","text"]) 
    b64dec_output = base64.b64decode(b64enc_output)
    with open(kms_dec_file,'w') as h:
        print("Writing to %s"%kms_dec_file,file=sys.stderr)
        h.write(b64dec_output)

    os.unlink(b64dec_input_file)
    os.unlink(kms_enc_file)


def kms_encrypt_file(profile,kms_dec_file,kms_key="account-key"):
    #removes the original if successful
    kms_enc_file=kms_dec_file + ".kms"
    #TODO: this only works with bash (unix)
    if os.system("aws --profile %(profile)s kms encrypt --key-id alias/%(kms_key)s --plaintext fileb://%(kms_dec_file)s --output text --query CiphertextBlob > %(kms_enc_file)s" % locals()) == 0:
        os.unlink(kms_dec_file)
    else:
        raise Exception("Could not encrypt %(kms_dec_file)s."%locals())

def foo():
    return "bla"

