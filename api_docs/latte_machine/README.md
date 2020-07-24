# Latte-Machine API

API documentation for latte-machine app

## Security

This api uses Auth0 as an IAM service provider. Below the details of this setup

### Setup Auth0

1. Create a new Auth0 Account
2. Select a unique tenant domain
3. Create a new, single page web application
4. Create a new API
   - in API Settings:
     - Enable RBAC
     - Enable Add Permissions in the Access Token
5. Create new API permissions:
   - `get:latte`
   - `post:latte`
   - `patch:latte`
   - `delete:latte`

## API Examples

**GET /api/latte**
Get all lattes

```bash
curl --location --request GET 'localhost:5000/api/latte'
```

**Response**

```json
{
  "lattes": {
    "id": 1,
    "ingredients": [
      {
        "name": "juice",
        "color": "orange",
        "parts": 3
      },
      {
        "name": "ice",
        "color": "blue",
        "parts": 1
      }
    ],
    "title": "Celestial"
  }
}
```

**GET /api/latte/1**
Get a specific latte

```bash
curl --location --request GET 'localhost:5000/api/latte/1'
```

**Response**

```json
{
  "lattes": {
    "id": 1,
    "ingredients": [
      {
        "name": "juice",
        "color": "orange",
        "parts": 3
      },
      {
        "name": "ice",
        "color": "blue",
        "parts": 1
      }
    ],
    "title": "Celestial"
  }
}
```

**POST /api/latte**
Create new latte

```bash
curl --location --request POST 'localhost:5000/api/latte' \
--header 'Authorization: Bearer Token' \
--header 'Content-Type: application/json' \
--data-raw '{
  "lattes": {
    "id": 1,
    "ingredients": [
      {
        "name": "juice",
        "color": "orange",
        "parts": 3
      },
      {
        "name": "ice",
        "color": "blue",
        "parts": 1
      }
    ],
    "title": "Celestial"
  }
}'
```

**Response**

```json
{
  "lattes": {
    "id": 1,
    "ingredients": [
      {
        "name": "juice",
        "color": "orange",
        "parts": 3
      },
      {
        "name": "ice",
        "color": "blue",
        "parts": 1
      }
    ],
    "title": "Celestial"
  }
}
```

**DELETE /api/latte/1**
Remove latte from database

```bash
curl --location --request DELETE 'localhost:5000/api/latte/1' \
--header 'Authorization: Bearer Token'
```

**Response**

```json
{
  "delete": 1,
  "success": true
}
```

**PATCH /api/latte/1**
Update latte content

```bash
curl --location --request PATCH 'localhost:5000/api/latte/1' \
--header 'Authorization: Bearer Token' \
--header 'Content-Type: application/json' \
--data-raw '{
  "title": "Celestial",
  "ingredients": [
    {
      "name": "milk",
      "color": "white",
      "parts": 3
    },
    {
      "name": "ice",
      "color": "blue",
      "parts": 1
    },
    {
      "name": "water",
      "color": "light-blue",
      "parts": 1
    }
  ]
}'
```

**Response**

```json
{
  "lattes": [
    {
      "id": 1,
      "ingredients": [
        {
          "name": "milk",
          "color": "white",
          "parts": 3
        },
        {
          "name": "ice",
          "color": "blue",
          "parts": 1
        },
        {
          "name": "water",
          "color": "light-blue",
          "parts": 1
        }
      ],
      "title": "Celestial"
    }
  ],
  "success": true
}
```

## Error Codes

The error format expected from this API is as follows:

**Example response**

```json
{
  "error": 409,
  "message": "A conflict happened while processing the request. The resource might have been modified while the request was being processed.",
  "success": false
}
```
