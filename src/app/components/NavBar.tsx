// app/components/Navbar.tsx

'use client';

import { useState } from 'react';
import Link from 'next/link';

export default function Navbar() {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const toggleMenu = () => {
    setIsMenuOpen(!isMenuOpen);
  };

  return (
    <header className="bg-blue-600 p-4 text-white">
      <h1 className="text-3xl font-bold">Open Provisioner</h1>
      <nav className="bg-blue-600 p-4 shadow-md">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className={`md:flex space-x-6 ${isMenuOpen ? 'block' : 'hidden'} md:block`}>
              <Link href="/" className="text-white hover:text-gray-300">
                Home
              </Link>
              <Link href="/devices" className="text-white hover:text-gray-300">
                Dispositivos
              </Link>
              <Link href="/users" className="text-white hover:text-gray-300">
                Usuários
              </Link>
              <Link href="/automations" className="text-white hover:text-gray-300">
                Automações
              </Link>
              <Link href="/settings" className="text-white hover:text-gray-300">
                Configurações
              </Link>
            </div>
          </div>

          <div className="md:hidden">
            <button onClick={toggleMenu} className="text-white">
              <i className="fas fa-bars"></i>
            </button>
          </div>
        </div>
      </nav>
    </header>
  );
}
