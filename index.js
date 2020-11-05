import Link from 'next/link'

const Index = () => (
  <div >
    <h1>
      <span>
        Welcome to this
      </span>
      <span >
        Awesome Website
      </span>
    </h1>
    <div >
      <Link href="/Antispoofing">
        <a>
        View account settings
        </a>
      </Link>
    </div>
  </div>
)

export default Index
