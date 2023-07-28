import os
import requests

REGISTRY_DOMAIN = 'registry-1.docker.io'

def get_dockerhub_token(image, data):
    dockerhub_token = None
    try:
        base_url = 'https://auth.docker.io/'
        print(f'image: {image}')
        auth_url = base_url + \
            'token?service=registry.docker.io&' + \
            f'scope=repository:{image}:pull'

        res = requests.get(
            url=auth_url,
            data=data,
        )
        dockerhub_token = res.json()['token']
    except Exception as e:
        message = f'Unable to retrieve token for {image}: {e}'
        print(message)


    return dockerhub_token


def get_manifest_headers(image, tag, token, accept):
    manifest_headers = None
    print(f'get_manifest_headers - image: {image}')
    try:
        headers = {
            'Authorization': f'Bearer {token}',
            'Accept': accept,
        }
        v2_registry_url = f'https://{REGISTRY_DOMAIN}/v2/'
        manifest_url = v2_registry_url + f'{image}/manifests/{tag}'
        print(f'get_manifest_headers - manifest_url: {manifest_url}')
        res = requests.get(url=manifest_url, headers=headers)
        print(f'get_manifest_headers - res.content: {res.content}')
        manifest_headers = res.headers
    except Exception as e:
        message = f'Unable to get manifest headers for {image}:{tag} : {e}'
        print(message)

    return manifest_headers


def get_formatted_image_data(image):
    return [
        image,
        f'library/{image}',
        f'_/{image}',
    ]


def main():
    accept = 'application/vnd.oci.image.index.v1+json'
    image = 'python'
    tag = '3.9.5-slim-buster'

    data = {
        'username': os.environ['dockerhub_username'],
    	'password': os.environ['dockerhub_password'],
    }

    formatted_image_data = get_formatted_image_data(image)
    print(f'formatted_image_data: {formatted_image_data}')

    for image_data in formatted_image_data:
        print(f'image_data: {image_data}')
        dockerhub_token = get_dockerhub_token(image_data, data)
        print(f'dockerhub_token: {dockerhub_token}')
        manifest_headers = get_manifest_headers(image_data, tag, dockerhub_token, accept)
        print(f'manifest_headers: {manifest_headers}')

if __name__ == "__main__":
    main()