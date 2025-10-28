import { Box, Heading, VStack } from '@chakra-ui/react'
import { createFileRoute } from '@tanstack/react-router'

import CreateCategoryForm from '@/components/Categories/CreateCategoryForm'
import CategoryList from '@/components/Categories/CategoryList'

export const Route = createFileRoute('/_layout/categories')({
  component: Categories,
})

function Categories() {
  return (
    <VStack spacing={8} align="stretch">
      <Box>
        <Heading size="lg" mb={4}>
          Create Category
        </Heading>
        <CreateCategoryForm />
      </Box>
      <Box>
        <Heading size="lg" mb={4}>
          Existing Categories
        </Heading>
        <CategoryList />
      </Box>
    </VStack>
  )
}
