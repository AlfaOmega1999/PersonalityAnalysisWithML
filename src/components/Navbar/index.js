import React from 'react'
import {
    Nav,
    NavLink,
    Bars,
    NavMenu,
    NavBtn,
    NavBtnLink
  } from './NavbarElements';
  import logo from '../../images/MBTI.png';

const Navbar = () => {
  return (
    <>
      <Nav>
          <NavLink to="/">
          <img src={logo} className="App-logo" alt="logo" />
          </NavLink>
          <Bars />
          <NavMenu>
              <NavLink to="/about" >
                  About
              </NavLink>
              <NavLink to="/services" >
                  Services
              </NavLink>
              <NavLink to="/contact" >
                  Contact
              </NavLink>
          </NavMenu>
          <NavBtn>
              <NavBtnLink to="/signin">Sign In</NavBtnLink>
          </NavBtn>
      </Nav>
    </>
  )
}

export default Navbar
