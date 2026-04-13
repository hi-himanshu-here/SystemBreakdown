## ✅ Status

- [x] Signup API
- [x] Login API (JWT)
- [x] Protected Route
- [ ] Refresh Tokens
- [ ] Logout System



## 🔐 Authentication Flow

1. User signs up with username and password
2. User logs in and receives:
   - Access Token (short-lived)
   - Refresh Token (long-lived)
3. Client sends Access Token in headers:
   Authorization: Bearer <token>
4. Backend verifies token and authenticates user
5. Protected routes are accessible only with valid token

---

## 🔗 API Endpoints

### 1. Signup
POST /api/signup/

### 2. Login
POST /api/login/

### 3. Profile (Protected)
GET /api/profile/

Requires:
Authorization: Bearer <access_token>

---

## 🧠 System Design Considerations

### Token Expiry
- Access tokens expire after a fixed time
- Requires refresh mechanism for better UX

### Security Risks
- Token theft can lead to unauthorized access
- Mitigation:
  - Use HTTPS
  - Store tokens securely (httpOnly cookies)
  - Token rotation

### Stateless Architecture
- No session stored on server
- Easy horizontal scaling
- Suitable for distributed systems

---

## ⚠️ Scaling Challenges

### 1. Database Bottleneck
- Login requires DB lookup
- Solution:
  - Indexing
  - Read replicas

### 2. CPU Load (Password Hashing)
- Hashing is expensive at scale
- Solution:
  - Efficient hashing configs
  - Horizontal scaling

### 3. High Traffic (1M users)
- Risk of server overload
- Solution:
  - Load balancing
  - Multiple backend instances

---

## 🚀 Future Improvements

- Implement Refresh Token API
- Add token blacklisting (logout support)
- Store tokens in Redis
- Add email authentication
- Add rate limiting (prevent brute force attacks)

---

## 🧠 Key Learning

This project demonstrates:
- Stateless authentication using JWT
- Protected routes with middleware
- Real-world backend security challenges
- System design trade-offs in authentication systems